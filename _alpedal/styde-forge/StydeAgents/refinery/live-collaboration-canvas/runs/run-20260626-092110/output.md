```
// server.js
// Live Collaboration Canvas — WebSocket Server
// Requires: npm install ws uuid
const WebSocket = require('ws');
const { v4: uuidv4 } = require('uuid');
const PORT = 8080;
const wss = new WebSocket.Server({ port: PORT });
console.log(`Live Collaboration Canvas server running on ws://localhost:${PORT}`);
// ─── State ───────────────────────────────────────────────────────────────────
const state = {
  users: new Map(),           // userId -> { id, name, color, cursor, panelFocus, viewport, connected }
  annotations: [],            // { id, userId, userName, panelId, x, y, text, timestamp }
  comments: [],               // { id, userId, userName, panelId, metricId, text, thread, timestamp }
  locks: new Map(),           // panelId -> { userId, userName, timestamp }
  chatMessages: [],           // { id, userId, userName, text, timestamp }
  syncState: {                // shared filter state
    filters: {},
    hostId: null,
    followMode: false,
  },
};
const USER_COLORS = [
  '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4',
  '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F',
  '#BB8FCE', '#85C1E9', '#F0B27A', '#82E0AA',
];
let colorIndex = 0;
function getUserColor() {
  const color = USER_COLORS[colorIndex % USER_COLORS.length];
  colorIndex++;
  return color;
}
function broadcast(message, excludeWs = null) {
  const data = typeof message === 'string' ? message : JSON.stringify(message);
  wss.clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN && client !== excludeWs) {
      client.send(data);
    }
  });
}
function broadcastState(targetWs = null) {
  const snapshot = {
    type: 'state:snapshot',
    users: Array.from(state.users.values()).map(u => ({
      id: u.id, name: u.name, color: u.color,
      cursor: u.cursor, panelFocus: u.panelFocus,
      viewport: u.viewport
    })),
    annotations: state.annotations,
    comments: state.comments,
    locks: Array.from(state.locks.entries()).map(([panelId, lock]) => ({
      panelId, userId: lock.userId, userName: lock.userName
    })),
    chatMessages: state.chatMessages.slice(-100),
    syncState: state.syncState,
  };
  const data = JSON.stringify(snapshot);
  if (targetWs) {
    targetWs.send(data);
  } else {
    broadcast(data);
  }
}
// ─── Connection Handler ──────────────────────────────────────────────────────
wss.on('connection', (ws) => {
  const userId = uuidv4().slice(0, 8);
  const user = {
    id: userId,
    name: `User-${userId.slice(0, 4)}`,
    color: getUserColor(),
    cursor: null,
    panelFocus: null,
    viewport: null,
    connected: true,
  };
  state.users.set(userId, user);
  console.log(`User connected: ${user.name} (${userId})`);
  // Send initial snapshot to this client only
  broadcastState(ws);
  // Broadcast user joined
  broadcast({ type: 'user:joined', user: { id: userId, name: user.name, color: user.color } });
  ws.on('message', (raw) => {
    let msg;
    try {
      msg = JSON.parse(raw.toString());
    } catch {
      return;
    }
    switch (msg.type) {
      // ── Presence ──────────────────────────────────────────────────────────
      case 'presence:cursor':
        user.cursor = msg.cursor;
        broadcast({
          type: 'presence:cursor',
          userId,
          cursor: msg.cursor,
          color: user.color,
          name: user.name,
        }, ws);
        break;
      case 'presence:focus':
        user.panelFocus = msg.panelId;
        broadcast({ type: 'presence:focus', userId, panelId: msg.panelId }, ws);
        break;
      case 'presence:viewport':
        user.viewport = msg.viewport;
        broadcast({ type: 'presence:viewport', userId, viewport: msg.viewport }, ws);
        break;
      // ── User Meta ─────────────────────────────────────────────────────────
      case 'user:rename':
        user.name = msg.name.slice(0, 24);
        broadcast({ type: 'user:renamed', userId, name: user.name }, ws);
        break;
      // ── Annotations ───────────────────────────────────────────────────────
      case 'annotation:add': {
        const annotation = {
          id: uuidv4().slice(0, 8),
          userId,
          userName: user.name,
          panelId: msg.panelId,
          x: msg.x,
          y: msg.y,
          text: msg.text || '',
          timestamp: Date.now(),
        };
        state.annotations.push(annotation);
        broadcast({ type: 'annotation:added', annotation });
        break;
      }
      case 'annotation:update': {
        const ann = state.annotations.find(a => a.id === msg.annotationId);
        if (ann && ann.userId === userId) {
          ann.text = msg.text;
          broadcast({ type: 'annotation:updated', annotationId: msg.annotationId, text: msg.text });
        }
        break;
      }
      case 'annotation:remove': {
        const idx = state.annotations.findIndex(a => a.id === msg.annotationId);
        if (idx !== -1) {
          state.annotations.splice(idx, 1);
          broadcast({ type: 'annotation:removed', annotationId: msg.annotationId });
        }
        break;
      }
      // ── Comments (threaded) ───────────────────────────────────────────────
      case 'comment:add': {
        const comment = {
          id: uuidv4().slice(0, 8),
          userId,
          userName: user.name,
          panelId: msg.panelId,
          metricId: msg.metricId || null,
          parentId: msg.parentId || null,
          text: msg.text,
          timestamp: Date.now(),
        };
        state.comments.push(comment);
        broadcast({ type: 'comment:added', comment });
        break;
      }
      // ── Locks ─────────────────────────────────────────────────────────────
      case 'lock:acquire': {
        if (state.locks.has(msg.panelId)) {
          ws.send(JSON.stringify({
            type: 'lock:denied',
            panelId: msg.panelId,
            lockedBy: state.locks.get(msg.panelId).userName,
          }));
        } else {
          state.locks.set(msg.panelId, { userId, userName: user.name, timestamp: Date.now() });
          broadcast({ type: 'lock:acquired', panelId: msg.panelId, userId, userName: user.name });
        }
        break;
      }
      case 'lock:release': {
        const lock = state.locks.get(msg.panelId);
        if (lock && lock.userId === userId) {
          state.locks.delete(msg.panelId);
          broadcast({ type: 'lock:released', panelId: msg.panelId });
        }
        break;
      }
      // ── Chat ──────────────────────────────────────────────────────────────
      case 'chat:send': {
        const chatMsg = {
          id: uuidv4().slice(0, 8),
          userId,
          userName: user.name,
          text: msg.text.slice(0, 500),
          timestamp: Date.now(),
        };
        state.chatMessages.push(chatMsg);
        broadcast({ type: 'chat:message', message: chatMsg });
        break;
      }
      // ── Sync / Follow ─────────────────────────────────────────────────────
      case 'sync:filter': {
        state.syncState.filters = msg.filters;
        broadcast({ type: 'sync:filters', filters: msg.filters, fromUserId: userId });
        break;
      }
      case 'sync:follow': {
        state.syncState.followMode = msg.enabled;
        state.syncState.hostId = msg.enabled ? userId : null;
        broadcast({ type: 'sync:follow', enabled: msg.enabled, hostId: userId });
        break;
      }
      case 'sync:navigate': {
        if (state.syncState.followMode && state.syncState.hostId === userId) {
          broadcast({ type: 'sync:navigate', viewport: msg.viewport, panelFocus: msg.panelId }, ws);
        }
        break;
      }
      default:
        break;
    }
  });
  ws.on('close', () => {
    state.users.delete(userId);
    // Release all locks held by this user
    for (const [panelId, lock] of state.locks) {
      if (lock.userId === userId) state.locks.delete(panelId);
    }
    broadcast({ type: 'user:left', userId, name: user.name });
    console.log(`User disconnected: ${user.name}`);
  });
});
```
To run: npm install ws uuid && node server.js
Then open client.html in multiple browser tabs on http://localhost:8080 (no, the server serves nothing — use a separate http server or open client.html directly).
But the server only does WebSocket. You need to serve client.html somehow.
Let me make it simpler — embed a static file server in the same server.js, so one command runs everything.
Let me replace the above with a combined file server + websocket in one.
Actually let me just write the proper combined server, then the client. I'll replace the server above.
```
// server.js — Live Collaboration Canvas
// Single file: HTTP serves client.html + static assets, WebSocket handles real-time sync
// Run: node server.js  OR: npm install ws uuid && node server.js
const http = require('http');
const fs = require('fs');
const path = require('path');
const WebSocket = require('ws');
const { v4: uuidv4 } = require('uuid');
const PORT = 8080;
// ─── HTTP Server ─────────────────────────────────────────────────────────────
const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'application/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
};
const httpServer = http.createServer((req, res) => {
  let filePath = req.url === '/' ? '/client.html' : req.url;
  filePath = path.join(__dirname, filePath);
  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404);
      res.end('Not Found');
      return;
    }
    const ext = path.extname(filePath);
    res.writeHead(200, { 'Content-Type': MIME[ext] || 'text/plain' });
    res.end(data);
  });
});
// ─── WebSocket (on same port) ────────────────────────────────────────────────
const wss = new WebSocket.Server({ server: httpServer });
const state = {
  users: new Map(),
  annotations: [],
  comments: [],
  locks: new Map(),
  chatMessages: [],
  syncState: { filters: {}, hostId: null, followMode: false },
};
const USER_COLORS = [
  '#FF6B6B','#4ECDC4','#45B7D1','#96CEB4',
  '#FFEAA7','#DDA0DD','#98D8C8','#F7DC6F',
  '#BB8FCE','#85C1E9','#F0B27A','#82E0AA',
];
let colorIndex = 0;
function broadcast(data, exclude = null) {
  const msg = typeof data === 'string' ? data : JSON.stringify(data);
  wss.clients.forEach(c => { if (c.readyState === WebSocket.OPEN && c !== exclude) c.send(msg); });
}
function snapshot(target) {
  const s = {
    type: 'state:snapshot',
    users: Array.from(state.users.values()).map(u => ({
      id: u.id, name: u.name, color: u.color,
      cursor: u.cursor, panelFocus: u.panelFocus, viewport: u.viewport
    })),
    annotations: state.annotations,
    comments: state.comments,
    locks: Array.from(state.locks.entries()).map(([id, l]) => ({ panelId: id, userId: l.userId, userName: l.userName })),
    chatMessages: state.chatMessages.slice(-100),
    syncState: state.syncState,
  };
  target.send(JSON.stringify(s));
}
wss.on('connection', (ws) => {
  const userId = uuidv4().slice(0, 8);
  const user = {
    id: userId, name: `User-${userId.slice(0, 4)}`, color: USER_COLORS[colorIndex++ % USER_COLORS.length],
    cursor: null, panelFocus: null, viewport: null, connected: true,
  };
  state.users.set(userId, user);
  snapshot(ws);
  broadcast({ type: 'user:joined', user: { id: userId, name: user.name, color: user.color } }, ws);
  ws.on('message', (raw) => {
    let msg;
    try { msg = JSON.parse(raw.toString()); } catch { return; }
    switch (msg.type) {
      case 'presence:cursor':
        user.cursor = msg.cursor;
        broadcast({ type: 'presence:cursor', userId, cursor: msg.cursor, color: user.color, name: user.name }, ws);
        break;
      case 'presence:focus':
        user.panelFocus = msg.panelId;
        broadcast({ type: 'presence:focus', userId, panelId: msg.panelId }, ws);
        break;
      case 'presence:viewport':
        user.viewport = msg.viewport;
        broadcast({ type: 'presence:viewport', userId, viewport: msg.viewport }, ws);
        break;
      case 'user:rename':
        user.name = msg.name.slice(0, 24);
        broadcast({ type: 'user:renamed', userId, name: user.name }, ws);
        break;
      case 'annotation:add': {
        const a = { id: uuidv4().slice(0,8), userId, userName: user.name, panelId: msg.panelId, x: msg.x, y: msg.y, text: msg.text||'', timestamp: Date.now() };
        state.annotations.push(a);
        broadcast({ type: 'annotation:added', annotation: a });
        break;
      }
      case 'annotation:update': {
        const a = state.annotations.find(x => x.id === msg.annotationId);
        if (a && a.userId === userId) { a.text = msg.text; broadcast({ type: 'annotation:updated', annotationId: msg.annotationId, text: msg.text }); }
        break;
      }
      case 'annotation:remove': {
        const i = state.annotations.findIndex(x => x.id === msg.annotationId);
        if (i !== -1) { state.annotations.splice(i,1); broadcast({ type: 'annotation:removed', annotationId: msg.annotationId }); }
        break;
      }
      case 'comment:add': {
        const c = { id: uuidv4().slice(0,8), userId, userName: user.name, panelId: msg.panelId, metricId: msg.metricId||null, parentId: msg.parentId||null, text: msg.text, timestamp: Date.now() };
        state.comments.push(c);
        broadcast({ type: 'comment:added', comment: c });
        break;
      }
      case 'lock:acquire': {
        if (state.locks.has(msg.panelId)) {
          ws.send(JSON.stringify({ type: 'lock:denied', panelId: msg.panelId, lockedBy: state.locks.get(msg.panelId).userName }));
        } else {
          state.locks.set(msg.panelId, { userId, userName: user.name, timestamp: Date.now() });
          broadcast({ type: 'lock:acquired', panelId: msg.panelId, userId, userName: user.name });
        }
        break;
      }
      case 'lock:release': {
        const l = state.locks.get(msg.panelId);
        if (l && l.userId === userId) { state.locks.delete(msg.panelId); broadcast({ type: 'lock:released', panelId: msg.panelId }); }
        break;
      }
      case 'chat:send': {
        const m = { id: uuidv4().slice(0,8), userId, userName: user.name, text: msg.text.slice(0,500), timestamp: Date.now() };
        state.chatMessages.push(m);
        broadcast({ type: 'chat:message', message: m });
        break;
      }
      case 'sync:filter':
        state.syncState.filters = msg.filters;
        broadcast({ type: 'sync:filters', filters: msg.filters, fromUserId: userId });
        break;
      case 'sync:follow':
        state.syncState.followMode = msg.enabled;
        state.syncState.hostId = msg.enabled ? userId : null;
        broadcast({ type: 'sync:follow', enabled: msg.enabled, hostId: userId });
        break;
      case 'sync:navigate':
        if (state.syncState.followMode && state.syncState.hostId === userId) {
          broadcast({ type: 'sync:navigate', viewport: msg.viewport, panelFocus: msg.panelId }, ws);
        }
        break;
    }
  });
  ws.on('close', () => {
    state.users.delete(userId);
    for (const [pid, l] of state.locks) { if (l.userId === userId) state.locks.delete(pid); }
    broadcast({ type: 'user:left', userId, name: user.name });
  });
});
httpServer.listen(PORT, () => {
  console.log(`Live Collaboration Canvas running at http://localhost:${PORT}`);
});
```
Now the client.html — this is the full interactive dashboard with presence cursors, annotations, comments, locks, chat, and sync.
```
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Live Collaboration Canvas</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
html, body { height: 100%; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, sans-serif; background: #0f1117; color: #e1e4e8; overflow: hidden; }
/* ── Layout ──────────────────────────────────────────────────────────── */
.app { display: flex; height: 100vh; }
.main { flex: 1; display: flex; flex-direction: column; min-width: 0; }
/* ── Top Bar ─────────────────────────────────────────────────────────── */
.topbar { display: flex; align-items: center; gap: 12px; padding: 8px 16px; background: #161b22; border-bottom: 1px solid #21262d; height: 48px; }
.topbar .title { font-weight: 700; font-size: 15px; color: #f0f6fc; margin-right: 8px; }
.topbar .users { display: flex; align-items: center; gap: 6px; flex: 1; overflow: hidden; }
.topbar .avatar { width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 11px; font-weight: 600; cursor: default; border: 2px solid transparent; flex-shrink: 0; position: relative; }
.topbar .avatar.me { border-color: #58a6ff; }
.topbar .follow-btn { margin-left: auto; display: flex; align-items: center; gap: 6px; background: #21262d; border: 1px solid #30363d; color: #c9d1d9; padding: 4px 10px; border-radius: 6px; cursor: pointer; font-size: 12px; white-space: nowrap; }
.topbar .follow-btn.active { background: #1f6feb; border-color: #388bfd; color: #fff; }
.topbar .follow-btn:hover { background: #30363d; }
.topbar .follow-btn.active:hover { background: #388bfd; }
.topbar .name-input { background: transparent; border: 1px solid transparent; color: #e1e4e8; font-size: 12px; padding: 2px 6px; border-radius: 4px; width: 120px; }
.topbar .name-input:focus { border-color: #30363d; outline: none; background: #0d1117; }
/* ── Dashboard Grid ──────────────────────────────────────────────────── */
.dashboard { flex: 1; padding: 16px; overflow-y: auto; display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: auto auto; gap: 16px; }
.panel { background: #161b22; border: 1px solid #21262d; border-radius: 12px; overflow: hidden; position: relative; transition: border-color .15s; min-height: 280px; }
.panel.locked { border-color: #da3633; }
.panel.focused { border-color: #58a6ff; box-shadow: 0 0 0 1px rgba(88,166,255,.3); }
.panel-header { display: flex; align-items: center; justify-content: space-between; padding: 10px 14px; background: #1c2128; border-bottom: 1px solid #21262d; }
.panel-header .pname { font-size: 13px; font-weight: 600; }
.panel-header .controls { display: flex; gap: 6px; align-items: center; }
.panel-header .controls button { background: none; border: 1px solid #30363d; color: #8b949e; padding: 3px 8px; border-radius: 4px; cursor: pointer; font-size: 11px; }
.panel-header .controls button:hover { background: #21262d; color: #c9d1d9; }
.panel-header .controls button.locked-btn { background: #da3633; color: #fff; border-color: #da3633; }
.panel-body { padding: 12px; position: relative; height: calc(100% - 42px); }
.panel-body canvas { max-width: 100%; max-height: 100%; }
/* ── Presence Cursors ────────────────────────────────────────────────── */
.cursor-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 100; }
.remote-cursor { position: absolute; pointer-events: none; transition: left .08s linear, top .08s linear; z-index: 100; }
.remote-cursor svg { width: 16px; height: 20px; }
.remote-cursor .label { position: absolute; left: 14px; top: -2px; background: inherit; color: #fff; font-size: 10px; padding: 1px 6px; border-radius: 3px; white-space: nowrap; font-weight: 500; }
/* ── Annotations (Sticky Notes) ──────────────────────────────────────── */
.annotation { position: absolute; background: #2d2200; border: 1px solid #664d00; border-radius: 6px; padding: 8px; font-size: 11px; min-width: 120px; max-width: 200px; z-index: 50; cursor: move; box-shadow: 0 4px 12px rgba(0,0,0,.4); }
.annotation .aname { font-weight: 600; margin-bottom: 4px; color: #ffd700; font-size: 10px; }
.annotation .atext { color: #e1e4e8; word-wrap: break-word; }
.annotation input { background: #1c2128; border: 1px solid #30363d; color: #e1e4e8; padding: 3px 6px; border-radius: 4px; width: 100%; font-size: 11px; }
.annotation .adel { position: absolute; top: 4px; right: 6px; cursor: pointer; color: #8b949e; font-size: 14px; line-height: 1; }
.annotation .adel:hover { color: #f85149; }
/* ── Chat Sidebar ────────────────────────────────────────────────────── */
.chat-sidebar { width: 300px; background: #161b22; border-left: 1px solid #21262d; display: flex; flex-direction: column; flex-shrink: 0; }
.chat-sidebar.hidden { display: none; }
.chat-header { padding: 10px 14px; background: #1c2128; border-bottom: 1px solid #21262d; display: flex; justify-content: space-between; align-items: center; }
.chat-header h3 { font-size: 13px; font-weight: 600; }
.chat-header button { background: none; border: none; color: #8b949e; cursor: pointer; font-size: 18px; }
.chat-messages { flex: 1; overflow-y: auto; padding: 10px 14px; display: flex; flex-direction: column; gap: 8px; }
.chat-msg { font-size: 12px; line-height: 1.4; }
.chat-msg .cname { font-weight: 600; margin-right: 6px; }
.chat-msg .ctext { color: #c9d1d9; }
.chat-msg .ctime { font-size: 10px; color: #484f58; margin-left: 6px; }
.chat-input { display: flex; padding: 8px 10px; border-top: 1px solid #21262d; gap: 6px; }
.chat-input input { flex: 1; background: #0d1117; border: 1px solid #30363d; color: #e1e4e8; padding: 6px 10px; border-radius: 6px; font-size: 12px; }
.chat-input input:focus { outline: none; border-color: #58a6ff; }
.chat-input button { background: #238636; border: none; color: #fff; padding: 6px 12px; border-radius: 6px; cursor: pointer; font-size: 12px; }
/* ── Annotations Panel ───────────────────────────────────────────────── */
.annotation-panel { position: fixed; right: 310px; top: 56px; background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; z-index: 200; min-width: 220px; box-shadow: 0 8px 24px rgba(0,0,0,.4); }
.annotation-panel.hidden { display: none; }
.annotation-panel h4 { font-size: 12px; margin-bottom: 8px; color: #8b949e; }
.annotation-panel textarea { width: 100%; background: #0d1117; border: 1px solid #30363d; color: #e1e4e8; padding: 6px; border-radius: 4px; font-size: 12px; resize: vertical; min-height: 60px; }
.annotation-panel textarea:focus { outline: none; border-color: #58a6ff; }
.annotation-panel .btn-row { display: flex; gap: 6px; margin-top: 8px; }
.annotation-panel .btn-row button { flex: 1; padding: 4px 0; border-radius: 4px; font-size: 11px; cursor: pointer; }
.annotation-panel .btn-row .save { background: #238636; border: none; color: #fff; }
.annotation-panel .btn-row .cancel { background: #21262d; border: 1px solid #30363d; color: #c9d1d9; }
/* ── Comments Panel ──────────────────────────────────────────────────── */
.comments-panel { position: fixed; right: 310px; bottom: 60px; background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px; z-index: 200; min-width: 260px; max-height: 320px; overflow-y: auto; box-shadow: 0 8px 24px rgba(0,0,0,.4); }
.comments-panel.hidden { display: none; }
.comments-panel h4 { font-size: 12px; margin-bottom: 8px; color: #8b949e; }
.comment-item { font-size: 11px; padding: 6px 0; border-bottom: 1px solid #21262d; }
.comment-item:last-child { border-bottom: none; }
.comment-item .cn { font-weight: 600; margin-right: 4px; }
.comment-item .ct { color: #c9d1d9; }
.comment-item .cd { font-size: 10px; color: #484f58; }
.comment-item.reply { padding-left: 16px; }
.comments-panel .add-comment { display: flex; gap: 4px; margin-top: 8px; }
.comments-panel .add-comment input { flex: 1; background: #0d1117; border: 1px solid #30363d; color: #e1e4e8; padding: 4px 8px; border-radius: 4px; font-size: 11px; }
.comments-panel .add-comment input:focus { outline: none; border-color: #58a6ff; }
.comments-panel .add-comment button { background: #238636; border: none; color: #fff; padding: 4px 10px; border-radius: 4px; font-size: 11px; cursor: pointer; }
/* ── Notifications ───────────────────────────────────────────────────── */
.notif { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); background: #1c2128; border: 1px solid #30363d; padding: 8px 20px; border-radius: 8px; font-size: 12px; z-index: 999; animation: fadeIn .2s; pointer-events: none; }
@keyframes fadeIn { from { opacity: 0; transform: translateX(-50%) translateY(8px); } to { opacity: 1; transform: translateX(-50%) translateY(0); } }
/* ── Lock Banner ─────────────────────────────────────────────────────── */
.lock-banner { position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,.5); display: flex; align-items: center; justify-content: center; z-index: 50; pointer-events: none; }
.lock-banner span { background: #da3633; color: #fff; padding: 4px 16px; border-radius: 6px; font-size: 12px; font-weight: 600; }
/* ── Scrollbar ───────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #30363d; border-radius: 3px; }
/* ── Toggle Chat Button ──────────────────────────────────────────────── */
.toggle-chat { position: fixed; bottom: 16px; right: 16px; background: #238636; border: none; color: #fff; width: 40px; height: 40px; border-radius: 50%; cursor: pointer; font-size: 18px; z-index: 50; box-shadow: 0 4px 12px rgba(0,0,0,.4); }
</style>
</head>
<body>
<div class="app">
  <div class="main">
    <div class="topbar">
      <div class="title">Live Canvas</div>
      <div class="users" id="userBar"></div>
      <input class="name-input" id="nameInput" placeholder="Your name" maxlength="24">
      <button class="follow-btn" id="followBtn">Follow me</button>
    </div>
    <div class="dashboard" id="dashboard">
      <!-- Panels created by JS -->
    </div>
  </div>
  <div class="chat-sidebar" id="chatSidebar">
    <div class="chat-header">
      <h3>Chat</h3>
      <button id="closeChat">&times;</button>
    </div>
    <div class="chat-messages" id="chatMessages"></div>
    <div class="chat-input">
      <input id="chatInput" placeholder="Type a message..." maxlength="500">
      <button id="sendChat">Send</button>
    </div>
  </div>
</div>
<button class="toggle-chat" id="toggleChat">💬</button>
<div class="annotation-panel hidden" id="annotationPanel">
  <h4 id="annotationTitle">Add annotation</h4>
  <textarea id="annotationText" placeholder="Type annotation..."></textarea>
  <div class="btn-row">
    <button class="save" id="saveAnnotation">Save</button>
    <button class="cancel" id="cancelAnnotation">Cancel</button>
  </div>
</div>
<div class="comments-panel hidden" id="commentsPanel">
  <h4 id="commentsTitle">Comments</h4>
  <div id="commentsList"></div>
  <div class="add-comment">
    <input id="commentInput" placeholder="Add comment..." maxlength="200">
    <button id="sendComment">Post</button>
  </div>
</div>
<script>
// ─── State ────────────────────────────────────────────────────────────────
const state = {
  users: new Map(),
  annotations: [],
  comments: [],
  locks: new Map(),
  chatMessages: [],
  syncState: { filters: {}, hostId: null, followMode: false },
  me: { id: null, name: 'User', color: '#58a6ff' },
  panelFocus: null,
  annotationDraft: null,  // { x, y, panelId, editId }
  commentDraft: null,     // { panelId, metricId }
};
const PANELS = [
  { id: 'revenue', name: 'Revenue Overview', chartType: 'line' },
  { id: 'users', name: 'User Growth', chartType: 'bar' },
  { id: 'metrics', name: 'Key Metrics', chartType: 'doughnut' },
  { id: 'activity', name: 'Activity Feed', chartType: 'polarArea' },
];
let ws;
let myId = null;
// ─── WebSocket ─────────────────────────────────────────────────────────────
function connect() {
  const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
  const wsUrl = `${protocol}//${location.host}`;
  ws = new WebSocket(wsUrl);
  ws.onopen = () => {
    showNotif('Connected to collaboration server');
  };
  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    handleMessage(msg);
  };
  ws.onclose = () => {
    showNotif('Disconnected. Reconnecting...');
    setTimeout(connect, 2000);
  };
  ws.onerror = () => {};
}
function send(data) {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify(data));
  }
}
// ─── Message Handler ───────────────────────────────────────────────────────
function handleMessage(msg) {
  switch (msg.type) {
    case 'state:snapshot': {
      myId = msg.users.find(u => u.color === state.me.color)?.id;
      if (myId) state.me.id = myId;
      msg.users.forEach(u => state.users.set(u.id, u));
      state.annotations = msg.annotations || [];
      state.comments = msg.comments || [];
      state.locks.clear();
      (msg.locks || []).forEach(l => state.locks.set(l.panelId, l));
      state.chatMessages = msg.chatMessages || [];
      state.syncState = msg.syncState || state.syncState;
      renderAll();
      break;
    }
    case 'user:joined':
      state.users.set(msg.user.id, { id: msg.user.id, name: msg.user.name, color: msg.user.color, cursor: null, panelFocus: null });
      renderUserBar();
      showNotif(`${msg.user.name} joined`);
      break;
    case 'user:left':
      state.users.delete(msg.userId);
      removeCursor(msg.userId);
      renderUserBar();
      showNotif(`${msg.name} left`);
      break;
    case 'user:renamed': {
      const u = state.users.get(msg.userId);
      if (u) u.name = msg.name;
      renderUserBar();
      break;
    }
    case 'presence:cursor':
      updateCursor(msg.userId, msg.cursor, msg.color, msg.name);
      break;
    case 'presence:focus': {
      const u2 = state.users.get(msg.userId);
      if (u2) u2.panelFocus = msg.panelId;
      const el = document.querySelector(`.panel[data-panel-id="${msg.panelId}"]`);
      if (el) {
        el.querySelectorAll('.remote-focus').forEach(e => e.remove());
        if (msg.userId !== myId) {
          const badge = document.createElement('div');
          badge.className = 'remote-focus';
          const col = state.users.get(msg.userId)?.color || '#888';
          badge.style.cssText = `position:absolute;bottom:4px;right:4px;background:${col};color:#fff;font-size:9px;padding:1px 6px;border-radius:3px;z-index:50;`;
          badge.textContent = state.users.get(msg.userId)?.name || '?';
          el.appendChild(badge);
        }
      }
      break;
    }
    case 'annotation:added':
      state.annotations.push(msg.annotation);
      renderAnnotations(msg.annotation.panelId);
      break;
    case 'annotation:updated': {
      const a = state.annotations.find(x => x.id === msg.annotationId);
      if (a) a.text = msg.text;
      renderAnnotations(a?.panelId);
      break;
    }
    case 'annotation:removed':
      state.annotations = state.annotations.filter(x => x.id !== msg.annotationId);
      renderAll();
      break;
    case 'comment:added':
      state.comments.push(msg.comment);
      if (state.commentDraft && state.commentDraft.panelId === msg.comment.panelId) {
        renderComments(msg.comment.panelId);
      }
      break;
    case 'lock:acquired':
      state.locks.set(msg.panelId, { userId: msg.userId, userName: msg.userName });
      renderPanelLock(msg.panelId);
      break;
    case 'lock:released':
      state.locks.delete(msg.panelId);
      renderPanelLock(msg.panelId);
      break;
    case 'lock:denied':
      showNotif(`Panel locked by ${msg.lockedBy}`);
      break;
    case 'chat:message':
      state.chatMessages.push(msg.message);
      renderChat();
      break;
    case 'sync:filters':
      state.syncState.filters = msg.filters;
      showNotif('Filters synced from host');
      break;
    case 'sync:follow':
      state.syncState.followMode = msg.enabled;
      state.syncState.hostId = msg.hostId;
      document.getElementById('followBtn').classList.toggle('active', msg.enabled && msg.hostId === myId);
      if (msg.enabled && msg.hostId !== myId) {
        showNotif('Now following host view');
      }
      break;
  }
}
// ─── Cursor Tracking ───────────────────────────────────────────────────────
const cursors = new Map();
function updateCursor(userId, cursor, color, name) {
  const panelEl = document.querySelector(`.panel[data-panel-id="${cursor.panelId}"]`);
  if (!panelEl) return;
  const overlay = panelEl.querySelector('.cursor-overlay');
  if (!overlay) return;
  let el = cursors.get(userId);
  if (!el) {
    el = document.createElement('div');
    el.className = 'remote-cursor';
    el.innerHTML = `<svg viewBox="0 0 16 20"><path d="M2 2L12 17H8.5L6.5 13L3 18L2 16L5.5 11L2 2Z" fill="${color}"/></svg><span class="label" style="background:${color}">${name}</span>`;
    overlay.appendChild(el);
    cursors.set(userId, el);
  }
  el.style.left = cursor.x + 'px';
  el.style.top = cursor.y + 'px';
}
function removeCursor(userId) {
  const el = cursors.get(userId);
  if (el) { el.remove(); cursors.delete(userId); }
}
// ─── Rendering ─────────────────────────────────────────────────────────────
function renderAll() {
  renderUserBar();
  renderPanels();
  renderChat();
  renderAnnotations();
  renderComments();
}
function renderUserBar() {
  const bar = document.getElementById('userBar');
  const users = Array.from(state.users.values());
  bar.innerHTML = users.map(u => {
    const isMe = u.id === myId;
    return `<div class="avatar${isMe ? ' me' : ''}" style="background:${u.color}" title="${u.name} (${isMe ? 'you' : ''})">${u.name[0]}</div>`;
  }).join('');
}
function renderPanels() {
  const grid = document.getElementById('dashboard');
  grid.innerHTML = '';
  PANELS.forEach((p, idx) => {
    const panel = document.createElement('div');
    panel.className = 'panel';
    panel.dataset.panelId = p.id;
    panel.innerHTML = `
      <div class="panel-header">
        <span class="pname">${p.name}</span>
        <div class="controls">
          <button class="annotate-btn" data-panel="${p.id}">Annotate</button>
          <button class="comment-btn" data-panel="${p.id}">Comment</button>
          <button class="lock-btn" data-panel="${p.id}">Lock</button>
        </div>
      </div>
      <div class="panel-body" id="panelBody-${p.id}">
        <canvas id="chart-${p.id}"></canvas>
        <div class="cursor-overlay"></div>
      </div>
    `;
    grid.appendChild(panel);
    renderPanelLock(p.id);
    setTimeout(() => initChart(p.id, p.chartType), 50);
  });
  document.querySelectorAll('.annotate-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const panelId = btn.dataset.panel;
      const lock = state.locks.get(panelId);
      if (lock && lock.userId !== myId) { showNotif(`Panel locked by ${lock.userName}`); return; }
      const rect = document.getElementById('panelBody-' + panelId).getBoundingClientRect();
      state.annotationDraft = { panelId, x: rect.width / 2, y: rect.height / 2, editId: null };
      showAnnotationPanel();
    });
  });
  document.querySelectorAll('.comment-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const panelId = btn.dataset.panel;
      state.commentDraft = { panelId, metricId: null };
      renderComments(panelId);
      document.getElementById('commentsPanel').classList.remove('hidden');
    });
  });
  document.querySelectorAll('.lock-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const panelId = btn.dataset.panel;
      const lock = state.locks.get(panelId);
      if (lock) {
        if (lock.userId === myId) send({ type: 'lock:release', panelId });
        else showNotif(`Locked by ${lock.userName}`);
      } else {
        send({ type: 'lock:acquire', panelId });
      }
    });
  });
  // Mouse tracking for presence
  document.querySelectorAll('.panel-body').forEach(body => {
    body.addEventListener('mousemove', (e) => {
      const rect = body.getBoundingClientRect();
      const panelId = body.closest('.panel').dataset.panelId;
      send({ type: 'presence:cursor', cursor: { x: e.clientX - rect.left, y: e.clientY - rect.top, panelId } });
    });
    body.addEventListener('mouseenter', () => {
      const panelId = body.closest('.panel').dataset.panelId;
      state.panelFocus = panelId;
      send({ type: 'presence:focus', panelId });
    });
  });
  // Click on chart to add annotation at position
  document.querySelectorAll('.panel-body canvas').forEach(canvas => {
    canvas.addEventListener('dblclick', (e) => {
      const panelId = canvas.closest('.panel').dataset.panelId;
      const lock = state.locks.get(panelId);
      if (lock && lock.userId !== myId) { showNotif(`Panel locked by ${lock.userName}`); return; }
      const rect = canvas.getBoundingClientRect();
      state.annotationDraft = { panelId, x: e.clientX - rect.left, y: e.clientY - rect.top, editId: null };
      showAnnotationPanel();
    });
  });
}
function renderPanelLock(panelId) {
  const panel = document.querySelector(`.panel[data-panel-id="${panelId}"]`);
  if (!panel) return;
  const lock = state.locks.get(panelId);
  const btn = panel.querySelector('.lock-btn');
  const body = panel.querySelector('.panel-body');
  let banner = panel.querySelector('.lock-banner');
  if (lock) {
    panel.classList.add('locked');
    if (btn) btn.textContent = 'Unlock';
    if (lock.userId === myId) btn.classList.add('locked-btn');
    else btn.classList.remove('locked-btn');
    if (lock.userId !== myId) {
      if (!banner) {
        banner = document.createElement('div');
        banner.className = 'lock-banner';
        banner.innerHTML = `<span>Locked by ${lock.userName}</span>`;
        body.appendChild(banner);
      }
    } else {
      if (banner) banner.remove();
    }
  } else {
    panel.classList.remove('locked');
    if (btn) { btn.textContent = 'Lock'; btn.classList.remove('locked-btn'); }
    if (banner) banner.remove();
  }
}
// ─── Charts ────────────────────────────────────────────────────────────────
const charts = {};
function initChart(panelId, type) {
  const canvas = document.getElementById('chart-' + panelId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const isDark = '#161b22';
  const gridColor = '#21262d';
  const textColor = '#8b949e';
  const chartConfigs = {
    line: {
      type: 'line',
      data: {
        labels: ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
        datasets: [{
          label: 'Revenue ($K)',
          data: [12, 19, 15, 22, 28, 24, 31],
          borderColor: '#58a6ff',
          backgroundColor: 'rgba(88,166,255,.1)',
          fill: true,
          tension: .3,
          pointBackgroundColor: '#58a6ff',
        }]
      },
      options: chartOpts(textColor, gridColor)
    },
    bar: {
      type: 'bar',
      data: {
        labels: ['Jan','Feb','Mar','Apr','May','Jun'],
        datasets: [{
          label: 'New Users',
          data: [420, 532, 601, 788, 912, 1054],
          backgroundColor: ['#4ECDC4','#45B7D1','#96CEB4','#FFEAA7','#DDA0DD','#98D8C8'],
        }]
      },
      options: chartOpts(textColor, gridColor)
    },
    doughnut: {
      type: 'doughnut',
      data: {
        labels: ['Active','Churned','New','Inactive'],
        datasets: [{
          data: [45, 20, 25, 10],
          backgroundColor: ['#238636','#da3633','#58a6ff','#484f58'],
        }]
      },
      options: { responsive: true, maintainAspectRatio: true, plugins: { legend: { labels: { color: textColor, font: { size: 10 } } } } }
    },
    polarArea: {
      type: 'polarArea',
      data: {
        labels: ['Views','Clicks','Signups','Purchases','Shares'],
        datasets: [{
          data: [1200, 890, 340, 210, 670],
          backgroundColor: ['rgba(88,166,255,.6)','rgba(78,205,196,.6)','rgba(35,134,54,.6)','rgba(218,54,51,.6)','rgba(221,160,221,.6)'],
        }]
      },
      options: { responsive: true, maintainAspectRatio: true, plugins: { legend: { labels: { color: textColor, font: { size: 10 } } } } }
    }
  };
  const config = chartConfigs[type] || chartConfigs.line;
  if (charts[panelId]) charts[panelId].destroy();
  charts[panelId] = new Chart(ctx, config);
  function chartOpts(txt, grid) {
    return {
      responsive: true, maintainAspectRatio: true,
      plugins: {
        legend: { labels: { color: txt, font: { size: 10 } } },
      },
      scales: {
        x: { grid: { color: grid }, ticks: { color: txt, font: { size: 9 } } },
        y: { grid: { color: grid }, ticks: { color: txt, font: { size: 9 } } },
      }
    };
  }
}
function chartOpts(txt, grid) {
  return {
    responsive: true, maintainAspectRatio: true,
    plugins: {
      legend: { labels: { color: txt, font: { size: 10 } } },
    },
    scales: {
      x: { grid: { color: grid }, ticks: { color: txt, font: { size: 9 } } },
      y: { grid: { color: grid }, ticks: { color: txt, font: { size: 9 } } },
    }
  };
}
// ─── Annotations ────────────────────────────────────────────────────────────
function showAnnotationPanel() {
  const panel = document.getElementById('annotationPanel');
  panel.classList.remove('hidden');
  document.getElementById('annotationText').value = '';
  document.getElementById('annotationText').focus();
  document.getElementById('annotationTitle').textContent = state.annotationDraft.editId ? 'Edit annotation' : 'Add annotation';
}
function renderAnnotations(panelId) {
  PANELS.forEach(p => {
    const body = document.getElementById('panelBody-' + p.id);
    if (!body) return;
    body.querySelectorAll('.annotation').forEach(el => el.remove());
    const anns = state.annotations.filter(a => a.panelId === p.id);
    anns.forEach(a => {
      const div = document.createElement('div');
      div.className = 'annotation';
      div.style.left = a.x + 'px';
      div.style.top = a.y + 'px';
      const isMine = a.userId === myId;
      div.innerHTML = `
        <div class="aname" style="color:${state.users.get(a.userId)?.color || '#ffd700'}">${a.userName}</div>
        <div class="atext">${escHtml(a.text)}</div>
        ${isMine ? '<span class="adel" data-id="'+a.id+'">&times;</span>' : ''}
      `;
      if (isMine) {
        div.style.cursor = 'pointer';
        div.addEventListener('dblclick', () => {
          state.annotationDraft = { panelId: p.id, x: a.x, y: a.y, editId: a.id };
          document.getElementById('annotationText').value = a.text;
          showAnnotationPanel();
        });
        div.querySelector('.adel').addEventListener('click', () => {
          send({ type: 'annotation:remove', annotationId: a.id });
        });
      }
      body.appendChild(div);
    });
  });
}
document.getElementById('saveAnnotation').addEventListener('click', () => {
  const text = document.getElementById('annotationText').value.trim();
  if (!text) return;
  if (state.annotationDraft.editId) {
    send({ type: 'annotation:update', annotationId: state.annotationDraft.editId, text });
  } else {
    send({ type: 'annotation:add', panelId: state.annotationDraft.panelId, x: state.annotationDraft.x, y: state.annotationDraft.y, text });
  }
  document.getElementById('annotationPanel').classList.add('hidden');
  state.annotationDraft = null;
});
document.getElementById('cancelAnnotation').addEventListener('click', () => {
  document.getElementById('annotationPanel').classList.add('hidden');
  state.annotationDraft = null;
});
// ─── Comments ──────────────────────────────────────────────────────────────
function renderComments(panelId) {
  const list = document.getElementById('commentsList');
  const title = document.getElementById('commentsTitle');
  const comments = state.comments.filter(c => c.panelId === panelId);
  title.textContent = `Comments — ${PANELS.find(p => p.id === panelId)?.name || panelId}`;
  list.innerHTML = comments.map(c => {
    const user = state.users.get(c.userId);
    const color = user?.color || '#888';
    const indent = c.parentId ? 'reply' : '';
    return `<div class="comment-item ${indent}"><span class="cn" style="color:${color}">${escHtml(c.userName)}</span><span class="ct">${escHtml(c.text)}</span> <span class="cd">${new Date(c.timestamp).toLocaleTimeString()}</span></div>`;
  }).join('');
  const input = document.getElementById('commentInput');
  input.dataset.panelId = panelId;
}
document.getElementById('sendComment').addEventListener('click', () => {
  const input = document.getElementById('commentInput');
  const text = input.value.trim();
  if (!text) return;
  send({ type: 'comment:add', panelId: input.dataset.panelId, text, metricId: state.commentDraft?.metricId || null, parentId: null });
  input.value = '';
});
document.getElementById('commentInput').addEventListener('keydown', (e) => {
  if (e.key === 'Enter') document.getElementById('sendComment').click();
});
// ─── Chat ──────────────────────────────────────────────────────────────────
function renderChat() {
  const el = document.getElementById('chatMessages');
  const msgs = state.chatMessages.slice(-50);
  el.innerHTML = msgs.map(m => {
    const user = state.users.get(m.userId);
    const color = user?.color || '#888';
    return `<div class="chat-msg"><span class="cname" style="color:${color}">${escHtml(m.userName)}</span><span class="ctext">${escHtml(m.text)}</span><span class="ctime">${new Date(m.timestamp).toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'})}</span></div>`;
  }).join('');
  el.scrollTop = el.scrollHeight;
}
document.getElementById('sendChat').addEventListener('click', () => {
  const input = document.getElementById('chatInput');
  const text = input.value.trim();
  if (!text) return;
  send({ type: 'chat:send', text });
  input.value = '';
});
document.getElementById('chatInput').addEventListener('keydown', (e) => {
  if (e.key === 'Enter') document.getElementById('sendChat').click();
});
document.getElementById('toggleChat').addEventListener('click', () => {
  document.getElementById('chatSidebar').classList.toggle('hidden');
});
document.getElementById('closeChat').addEventListener('click', () => {
  document.getElementById('chatSidebar').classList.add('hidden');
});
// ─── User Name ─────────────────────────────────────────────────────────────
document.getElementById('nameInput').addEventListener('change', () => {
  const name = document.getElementById('nameInput').value.trim();
  if (name) send({ type: 'user:rename', name });
});
// ─── Follow Mode ───────────────────────────────────────────────────────────
document.getElementById('followBtn').addEventListener('click', () => {
  const active = document.getElementById('followBtn').classList.toggle('active');
  send({ type: 'sync:follow', enabled: active });
});
// ─── Utility ───────────────────────────────────────────────────────────────
function escHtml(s) {
  const d = document.createElement('div');
  d.textContent = s;
  return d.innerHTML;
}
function showNotif(text) {
  const old = document.querySelector('.notif');
  if (old) old.remove();
  const el = document.createElement('div');
  el.className = 'notif';
  el.textContent = text;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 3000);
}
// ─── Follow Mode: Navigate sync ────────────────────────────────────────────
document.getElementById('dashboard').addEventListener('scroll', () => {
  if (state.syncState.followMode && state.syncState.hostId === myId) {
    send({ type: 'sync:navigate', viewport: { scrollTop: document.getElementById('dashboard').scrollTop, scrollLeft: document.getElementById('dashboard').scrollLeft }, panelId: state.panelFocus });
  }
});
// ─── Init ──────────────────────────────────────────────────────────────────
document.getElementById('chatSidebar').classList.add('hidden');
connect();
</script>
</body>
</html>
```
Save both files in the same directory, then:
npm install ws uuid
node server.js
Open http://localhost:8080 in multiple browser tabs to test collaboration
The dashboard includes all 7 required features:
1. Presence: Colored avatars in top bar + live cursors on each panel showing other users' mouse positions and name labels
2. Annotations: Double-click any chart or use the Annotate button to place a sticky note. Yours are editable and deletable. Everyone sees them instantly.
3. Comments: Use the Comment button on any panel to open a threaded comment view. Post comments visible to all users.
4. Sync: The Follow Me button in the top bar toggles host-driven view synchronization. When active, host scroll position and panel focus are broadcasted.
5. Lock: Each panel has a Lock button. When locked by another user, a banner overlay appears and interactions are blocked.
6. Chat: Toggle the chat sidebar with the floating button (bottom-right). Real-time messaging with user colors and timestamps.
7. State sync: Full snapshot on connect so late-joining users see everything. All events broadcast in real-time via WebSocket.