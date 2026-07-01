"""
Integration tests for dashboard-auth-specialist.
Exercises the full HTTP request-response cycle end-to-end.
"""

import base64
import http.cookiejar
import json
import os
import sys
import threading
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dashboard_auth as auth

PORT = 19823
BASE = f'http://127.0.0.1:{PORT}'

server = None
server_thread = None


def setup_module():
    auth.init_db()
    auth.configure(
        cors_allowed_origins=['http://dashboard.local'],
        require_https=False,
        session_expiry=3600,
        session_renew_threshold=300,
        rate_limit_max_requests=100,
        rate_limit_window=60,
    )
    auth.create_user('integration', 'testpass123')

    class TestApp(auth.DashboardBaseHandler):
        def do_GET(self):
            if self.path == '/':
                self.send_json({'status': 'ok', 'endpoint': 'public'})
            elif self.path == '/dashboard':
                self.handle_dashboard()
            elif self.path == '/csrf-refresh':
                self.handle_csrf_refresh()
            else:
                self.send_json({'error': 'Not Found'}, 404)

        @auth.auth_required(require_csrf=False)
        def handle_dashboard(self):
            csrf = auth.get_csrf_token(self._session)
            self.send_json({
                'message': 'dashboard',
                'user_id': self._session['user_id'],
                'csrf_token': csrf,
            })

        @auth.auth_required(require_csrf=False)
        def handle_csrf_refresh(self):
            csrf = auth.get_csrf_token(self._session)
            self.send_json({'csrf_token': csrf})

        def do_POST(self):
            if self.path == '/login':
                self.handle_login()
            elif self.path == '/data':
                self.handle_create_data()
            elif self.path == '/logout':
                self.handle_logout()
            else:
                self.send_json({'error': 'Not Found'}, 404)

        def handle_login(self):
            body = getattr(self, '_parsed_body', {})
            username = auth.sanitize_string(body.get('username', ''), 64)
            password = body.get('password', '')
            # Also check Authorization header for Basic Auth
            auth_header = self.headers.get('Authorization', '')
            if not username and auth_header.startswith('Basic '):
                creds = auth.parse_basic_auth(auth_header)
                if creds:
                    username, password = creds
            if not username or not password:
                self.send_json({'error': 'Missing credentials'}, 400)
                return
            if not auth.validate_input(username, 'username'):
                self.send_json({'error': 'Invalid username'}, 400)
                return
            user_id = auth.authenticate_user(username, password)
            if user_id is None:
                self.send_json({'error': 'Invalid credentials'}, 401)
                return
            sd = auth.create_session(user_id)
            # get_csrf_token may renew the token — update sd so cookie matches body
            csrf = auth.get_csrf_token(sd)
            sd['csrf_token'] = csrf
            sd['csrf_created'] = time.time()
            self._session_data = sd
            self._new_session = True
            self.send_json({
                'message': 'Login successful',
                'user_id': user_id,
                'csrf_token': csrf,
            })

        @auth.auth_required(require_csrf=True)
        def handle_create_data(self):
            body = getattr(self, '_parsed_body', {})
            data = auth.sanitize_string(body.get('data', ''))
            self.send_json({'message': 'Data created', 'data': data}, 201)

        @auth.auth_required(require_csrf=True)
        def handle_logout(self):
            cookies = auth.parse_cookies(self.headers.get('Cookie', ''))
            auth.delete_session(cookies.get('session_id', ''))
            self.send_json({'message': 'Logged out'})

        def do_PUT(self):
            if self.path == '/data':
                self.handle_update_data()
            else:
                self.send_json({'error': 'Not Found'}, 404)

        @auth.auth_required(require_csrf=True)
        def handle_update_data(self):
            body = getattr(self, '_parsed_body', {})
            data = auth.sanitize_string(body.get('data', ''))
            self.send_json({'message': 'Data updated', 'data': data})

        def do_DELETE(self):
            if self.path == '/data':
                self.handle_delete_data()
            else:
                self.send_json({'error': 'Not Found'}, 404)

        @auth.auth_required(require_csrf=True)
        def handle_delete_data(self):
            self.send_json({'message': 'Data deleted'})

    global server
    server = auth.HTTPServer(('127.0.0.1', PORT), TestApp)
    server.timeout = 0.5
    global server_thread
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    time.sleep(0.3)
    print(f'Server running on {BASE}')


def teardown_module():
    global server
    if server:
        server.shutdown()
        server.server_close()


def _opener():
    """Create an opener that preserves cookies across requests."""
    cj = http.cookiejar.CookieJar()
    return urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(cj)
    ), cj


def _req(method, path, data=None, headers=None, opener=None):
    """Make an HTTP request. If opener provided, cookies persist."""
    url = f'{BASE}{path}'
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(url, data=body, method=method,
                                  headers=headers or {})
    if data is not None and 'Content-Type' not in (headers or {}):
        req.add_header('Content-Type', 'application/json')
    try:
        opener_to_use = opener or urllib.request.build_opener()
        resp = opener_to_use.open(req, timeout=5)
        raw = resp.read().decode()
        return resp.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        return e.code, json.loads(raw) if raw else {}
    except urllib.error.URLError as e:
        return 0, {'error': str(e.reason)}


def _login(opener, cj):
    """Login using JSON body + Basic Auth via the provided opener.
    Returns the response data (which includes csrf_token).
    After this call, cj holds the session cookie."""
    creds = base64.b64encode(b'integration:testpass123').decode()
    status, data = _req('POST', '/login', {
        'username': 'integration',
        'password': 'testpass123',
    }, headers={'Authorization': f'Basic {creds}'}, opener=opener)
    assert status == 200, f'Login failed: {status} {data}'
    return data


# ═══════════════════════════════════════════════════════════════════════════════
# Tests
# ═══════════════════════════════════════════════════════════════════════════════

def test_public_endpoint():
    status, data = _req('GET', '/')
    assert status == 200
    assert data['status'] == 'ok'
    print('[INTEGRATION PASS] public endpoint')


def test_unauthenticated_blocked():
    status, data = _req('GET', '/dashboard')
    assert status == 401, f'Expected 401, got {status}: {data}'
    print('[INTEGRATION PASS] unauthenticated request blocked with 401')


def test_login_sets_cookies():
    opener, cj = _opener()
    data = _login(opener, cj)
    # CookieJar should have session_id and csrf_token
    cookies = list(cj)
    assert len(cookies) >= 1, f'Expected cookies, got {len(cookies)}'
    cookie_names = {c.name for c in cookies}
    assert 'session_id' in cookie_names, f'No session_id cookie in {cookie_names}'
    print(f'[INTEGRATION PASS] login sets cookies: {cookie_names}')


def test_authenticated_endpoint():
    opener, cj = _opener()
    _login(opener, cj)
    status, data = _req('GET', '/dashboard', opener=opener)
    assert status == 200, f'Expected 200, got {status}: {data}'
    assert data['message'] == 'dashboard'
    assert 'user_id' in data
    print(f'[INTEGRATION PASS] authenticated endpoint (user_id={data["user_id"]})')


def test_csrf_valid_on_post():
    opener, cj = _opener()
    login_data = _login(opener, cj)
    csrf = login_data['csrf_token']
    status, data = _req('POST', '/data', data={'data': 'hello'},
                         headers={'X-CSRF-Token': csrf}, opener=opener)
    assert status == 201, f'Expected 201, got {status}: {data}'
    assert data['message'] == 'Data created'
    assert data['data'] == 'hello'
    print('[INTEGRATION PASS] POST with valid CSRF token')


def test_csrf_invalid_returns_403():
    opener, cj = _opener()
    _login(opener, cj)
    status, data = _req('POST', '/data', data={'data': 'x'},
                         headers={'X-CSRF-Token': 'INVALID'}, opener=opener)
    assert status == 403, f'Expected 403, got {status}: {data}'
    print('[INTEGRATION PASS] POST with invalid CSRF blocked (403)')


def test_csrf_missing_returns_403():
    opener, cj = _opener()
    _login(opener, cj)
    status, data = _req('POST', '/data', data={'data': 'x'}, opener=opener)
    assert status == 403, f'Expected 403, got {status}: {data}'
    print('[INTEGRATION PASS] POST without CSRF blocked (403)')


def test_logout_invalidates_session():
    opener, cj = _opener()
    login_data = _login(opener, cj)
    csrf = login_data['csrf_token']
    status, data = _req('POST', '/logout', data={},
                         headers={'X-CSRF-Token': csrf}, opener=opener)
    assert status == 200, f'Logout failed: {status} {data}'
    status, data = _req('GET', '/dashboard', opener=opener)
    assert status == 401, f'Expected 401 after logout, got {status}'
    print('[INTEGRATION PASS] logout invalidates session')


def test_xss_sanitized():
    opener, cj = _opener()
    login_data = _login(opener, cj)
    csrf = login_data['csrf_token']
    payload = '<script>alert("xss")</script>'
    status, data = _req('POST', '/data', data={'data': payload},
                         headers={'X-CSRF-Token': csrf}, opener=opener)
    assert status == 201
    sanitized = data['data']
    assert '&lt;' in sanitized, f'Expected escaped output, got: {sanitized}'
    assert '<script>' not in sanitized, 'XSS was NOT sanitized!'
    print('[INTEGRATION PASS] XSS input sanitized')


def test_put_csrf_required():
    opener, cj = _opener()
    login_data = _login(opener, cj)
    csrf = login_data['csrf_token']
    status, data = _req('PUT', '/data', data={'data': 'updated'},
                         headers={'X-CSRF-Token': csrf}, opener=opener)
    assert status == 200, f'Expected 200, got {status}: {data}'
    assert data['message'] == 'Data updated'
    # PUT without CSRF should fail
    status, data = _req('PUT', '/data', data={'data': 'x'}, opener=opener)
    assert status == 403, f'Expected 403, got {status}'
    print('[INTEGRATION PASS] PUT requires CSRF')


def test_delete_csrf_required():
    opener, cj = _opener()
    login_data = _login(opener, cj)
    csrf = login_data['csrf_token']
    status, data = _req('DELETE', '/data',
                         headers={'X-CSRF-Token': csrf}, opener=opener)
    assert status == 200, f'Expected 200, got {status}: {data}'
    # DELETE without CSRF should fail
    status, data = _req('DELETE', '/data', opener=opener)
    assert status == 403, f'Expected 403, got {status}'
    print('[INTEGRATION PASS] DELETE requires CSRF')


def test_not_found():
    status, data = _req('GET', '/nonexistent')
    assert status == 404, f'Expected 404, got {status}'
    print('[INTEGRATION PASS] 404 for unknown route')


def test_options_preflight():
    status, data = _req('OPTIONS', '/')
    assert status == 204, f'Expected 204, got {status}'
    print('[INTEGRATION PASS] OPTIONS preflight returns 204')


def test_csrf_refresh():
    opener, cj = _opener()
    login_data = _login(opener, cj)
    csrf1 = login_data['csrf_token']
    status, data = _req('GET', '/csrf-refresh', opener=opener)
    assert status == 200
    csrf2 = data['csrf_token']
    assert csrf2, 'Expected csrf_token in response'
    print(f'[INTEGRATION PASS] CSRF token refreshed (len={len(csrf2)})')


def test_csrf_token_reused_works():
    """Same CSRF token can be reused within expiry window."""
    opener, cj = _opener()
    login_data = _login(opener, cj)
    csrf = login_data['csrf_token']
    # First POST
    status, data = _req('POST', '/data', data={'data': 'first'},
                         headers={'X-CSRF-Token': csrf}, opener=opener)
    assert status == 201
    # Second POST with same token
    status, data = _req('POST', '/data', data={'data': 'second'},
                         headers={'X-CSRF-Token': csrf}, opener=opener)
    assert status == 201, f'CSRF token reuse failed: {status} {data}'
    print('[INTEGRATION PASS] CSRF token can be reused within window')


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    setup_module()
    passed = 0
    failed = 0
    tests = [
        test_public_endpoint,
        test_unauthenticated_blocked,
        test_login_sets_cookies,
        test_authenticated_endpoint,
        test_csrf_valid_on_post,
        test_csrf_invalid_returns_403,
        test_csrf_missing_returns_403,
        test_put_csrf_required,
        test_delete_csrf_required,
        test_csrf_refresh,
        test_csrf_token_reused_works,
        test_logout_invalidates_session,
        test_xss_sanitized,
        test_not_found,
        test_options_preflight,
    ]
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f'[INTEGRATION FAIL] {test.__name__}: {e}')
            import traceback
            traceback.print_exc()
            failed += 1
    total = passed + failed
    print(f'\nIntegration: {passed}/{total} passed, {failed} failed')
    teardown_module()
    assert failed == 0, f'{failed} integration test(s) failed'
    print('All integration tests passed.')
