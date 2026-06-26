# Project Management SaaS — REST API Design

**Version:** 1.0.0  
**Base URL:** `https://api.promgr.example.com/v1`  
**Date:** 2026-06-25  
**Architect:** API Architect Agent

---

## Table of Contents

1. [Resource Model](#1-resource-model)
2. [Authentication & Authorization](#2-authentication--authorization)
3. [Pagination Strategy](#3-pagination-strategy)
4. [Error Handling](#4-error-handling)
5. [Endpoint Definitions](#5-endpoint-definitions)
6. [Request/Response Schemas](#6-requestresponse-schemas)
7. [OpenAPI 3.0 Specification](#7-openapi-30-specification)

---

## 1. Resource Model

### 1.1 Entity-Relationship Overview

```
┌──────────┐       ┌──────────────┐       ┌──────────┐
│   User   │◄──────┤  Membership  ├──────►│   Team   │
└────┬─────┘       └──────────────┘       └────┬─────┘
     │                                         │
     │  assigned_to                            │  owns
     ▼                                         ▼
┌──────────┐                          ┌──────────────┐
│   Task   │◄─────────────────────────│   Project    │
└────┬─────┘     belongs_to           └──────────────┘
     │
     │  parent_task (self-ref)
     ▼
┌──────────┐
│ Sub-task │
└──────────┘
```

### 1.2 Core Resources

| Resource    | Description                                              | Key Attributes                                                                 |
|-------------|----------------------------------------------------------|--------------------------------------------------------------------------------|
| **User**    | Individual account holder                                | `id`, `email`, `name`, `avatar_url`, `role`, `created_at`, `updated_at`        |
| **Team**    | Group of users collaborating on projects                 | `id`, `name`, `slug`, `description`, `owner_id`, `created_at`, `updated_at`    |
| **Project** | Top-level work container owned by a team                 | `id`, `name`, `slug`, `description`, `team_id`, `status`, `start_date`, `due_date`, `created_at`, `updated_at` |
| **Task**    | Unit of work within a project; supports nesting          | `id`, `title`, `description`, `project_id`, `assignee_id`, `parent_task_id`, `status`, `priority`, `estimated_hours`, `actual_hours`, `due_date`, `order`, `created_at`, `updated_at` |
| **Comment** | Discussion thread entry on a task                        | `id`, `task_id`, `author_id`, `body`, `created_at`, `updated_at`               |

### 1.3 Auxiliary Resources

| Resource        | Description                                |
|-----------------|--------------------------------------------|
| **Membership**  | Join table between User and Team with `role` (owner, admin, member, viewer) |
| **Tag**         | Label applied to tasks/projects            |
| **Attachment**  | File linked to a task                      |
| **ActivityLog** | Audit trail of resource mutations          |

### 1.4 Enumerations

```yaml
UserRole:
  - super_admin   # Platform-level
  - user          # Default

MembershipRole:
  - owner         # Full team control
  - admin         # Manage members, projects
  - member        # Create/edit tasks
  - viewer        # Read-only

ProjectStatus:
  - active
  - archived
  - completed
  - on_hold

TaskStatus:
  - backlog
  - todo
  - in_progress
  - in_review
  - done
  - cancelled

TaskPriority:
  - critical
  - high
  - medium
  - low
```

---

## 2. Authentication & Authorization

### 2.1 JWT Token Flow

```
┌──────────┐                              ┌──────────┐
│  Client  │                              │   API    │
└────┬─────┘                              └────┬─────┘
     │  POST /auth/login                       │
     │  { email, password }                    │
     │────────────────────────────────────────►│
     │                                         │
     │  200 OK                                 │
     │  { access_token, refresh_token,         │
     │    expires_in, token_type }             │
     │◄────────────────────────────────────────│
     │                                         │
     │  GET /projects                          │
     │  Authorization: Bearer <access_token>   │
     │────────────────────────────────────────►│
     │                                         │
     │  200 OK (projects list)                 │
     │◄────────────────────────────────────────│
     │                                         │
     │  POST /auth/refresh                     │
     │  { refresh_token }                      │
     │────────────────────────────────────────►│
     │                                         │
     │  200 OK                                 │
     │  { access_token, refresh_token,         │
     │    expires_in }                         │
     │◄────────────────────────────────────────│
```

### 2.2 Token Configuration

| Parameter                | Value        | Description                              |
|--------------------------|--------------|------------------------------------------|
| Access token lifetime    | 15 minutes   | Short-lived for security                 |
| Refresh token lifetime   | 14 days      | Rotated on each refresh                  |
| Token type               | `Bearer`     | Standard Authorization header prefix     |
| Signing algorithm        | `RS256`      | Asymmetric (public/private key pair)     |
| Token issuer             | `promgr-api` | `iss` claim                              |
| Token audience           | `promgr-app` | `aud` claim                              |

### 2.3 JWT Payload Structure

```json
{
  "iss": "promgr-api",
  "aud": "promgr-app",
  "sub": "usr_a1b2c3d4",
  "iat": 1719356400,
  "exp": 1719357300,
  "jti": "jti_9f8e7d6c",
  "email": "alice@example.com",
  "role": "user",
  "memberships": {
    "team_x": "admin",
    "team_y": "member"
  }
}
```

### 2.4 Authorization Middleware Logic

```
1. Extract Bearer token from Authorization header
2. Validate signature (RS256) and claims (iss, aud, exp, nbf)
3. If invalid/expired → 401 Unauthorized
4. Extract user_id (sub claim) and memberships
5. For team-scoped endpoints:
   a. Check if user's memberships include the target team
   b. Check if membership role satisfies required minimum role
   c. If not → 403 Forbidden
6. Inject authenticated context into request
```

### 2.5 Auth Endpoints

| Method   | Path                | Description              | Auth Required |
|----------|---------------------|--------------------------|---------------|
| `POST`   | `/auth/register`    | Create new user account  | No            |
| `POST`   | `/auth/login`       | Authenticate, get tokens | No            |
| `POST`   | `/auth/refresh`     | Rotate tokens            | No (uses refresh token) |
| `POST`   | `/auth/logout`      | Invalidate refresh token | Yes           |
| `POST`   | `/auth/forgot-password` | Send reset email     | No            |
| `POST`   | `/auth/reset-password`  | Set new password     | No (uses reset token) |
| `GET`    | `/auth/me`          | Get current user profile | Yes           |

---

## 3. Pagination Strategy

### 3.1 Cursor-Based Pagination

All list endpoints use cursor-based pagination for consistency and performance under high write loads.

**Why cursor-based:**
- Stable results even as records are inserted/deleted (no skipped or duplicate items)
- Efficient for large datasets (no `OFFSET` scans)
- Works with real-time feeds

### 3.2 Request Parameters

| Parameter  | Type    | Default | Description                                    |
|------------|---------|---------|------------------------------------------------|
| `cursor`   | string  | null    | Opaque cursor from previous response           |
| `limit`    | integer | 25      | Items per page (min: 1, max: 100)              |
| `sort`     | string  | varies  | Sort field and direction (e.g., `-created_at`) |
| `direction`| string  | `next`  | `next` for forward, `prev` for backward        |

### 3.3 Response Envelope

```json
{
  "data": [
    { "id": "prj_...", "name": "..." }
  ],
  "pagination": {
    "next_cursor": "eyJpZCI6InByal84ODgifQ==",
    "prev_cursor": null,
    "has_next": true,
    "has_prev": false,
    "total_count": 142,
    "limit": 25
  }
}
```

| Field          | Type    | Description                                      |
|----------------|---------|--------------------------------------------------|
| `next_cursor`  | string\|null | Cursor for the next page; `null` if last page |
| `prev_cursor`  | string\|null | Cursor for the previous page; `null` if first   |
| `has_next`     | boolean | Whether more items exist after this page         |
| `has_prev`     | boolean | Whether items exist before this page             |
| `total_count`  | integer | Total matching items (optional; may be omitted for performance) |
| `limit`        | integer | Echo of the limit used                           |

### 3.4 Cursor Implementation

```python
# Cursor is a base64-encoded JSON object containing the sort key
# of the last item on the current page. This makes cursors opaque
# to clients but meaningful to the server.

import base64, json

def encode_cursor(item, sort_field="created_at", sort_desc=True):
    payload = {
        "v": str(item[sort_field]) if sort_field in item else "",
        "id": item["id"],
        "d": sort_desc
    }
    return base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")

def decode_cursor(cursor_str):
    # Add padding back
    padded = cursor_str + "=" * (4 - len(cursor_str) % 4)
    return json.loads(base64.urlsafe_b64decode(padded))
```

### 3.5 Link Header (RFC 8288)

As a secondary mechanism, the API includes `Link` headers:

```http
Link: <https://api.promgr.example.com/v1/projects?cursor=abc123&limit=25>; rel="next"
Link: <https://api.promgr.example.com/v1/projects?cursor=xyz789&limit=25&direction=prev>; rel="prev"
```

---

## 4. Error Handling

### 4.1 Error Response Format

All errors follow a consistent JSON structure:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "One or more fields failed validation.",
    "request_id": "req_9f8e7d6c5b4a",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "Must be a valid email address."
      },
      {
        "field": "password",
        "code": "TOO_SHORT",
        "message": "Must be at least 8 characters."
      }
    ]
  }
}
```

### 4.2 Top-Level Error Fields

| Field        | Type   | Description                                              |
|--------------|--------|----------------------------------------------------------|
| `code`       | string | Machine-readable error code (dotted notation)            |
| `message`    | string | Human-readable summary                                   |
| `request_id` | string | Unique request identifier for tracing/log correlation    |
| `details`    | array  | (Optional) Field-level or sub-errors                     |

### 4.3 HTTP Status Code Usage

| Code | Name                  | When Used                                                |
|------|-----------------------|----------------------------------------------------------|
| 200  | OK                    | Successful GET, PUT, PATCH                               |
| 201  | Created               | Successful POST (resource created)                       |
| 204  | No Content            | Successful DELETE                                        |
| 400  | Bad Request           | Malformed JSON, invalid query parameters                 |
| 401  | Unauthorized          | Missing or invalid token                                 |
| 403  | Forbidden             | Valid token but insufficient permissions                 |
| 404  | Not Found             | Resource does not exist                                  |
| 409  | Conflict              | Duplicate resource, version conflict, state violation    |
| 422  | Unprocessable Entity  | Validation failure (well-formed request, semantic error) |
| 429  | Too Many Requests     | Rate limit exceeded                                      |
| 500  | Internal Server Error | Unexpected server failure                                |
| 503  | Service Unavailable   | Maintenance mode, upstream dependency down               |

### 4.4 Error Code Catalog

| Error Code                      | HTTP | Meaning                                       |
|---------------------------------|------|-----------------------------------------------|
| `AUTH_INVALID_CREDENTIALS`      | 401  | Wrong email or password                       |
| `AUTH_TOKEN_EXPIRED`            | 401  | Access token past its `exp` claim             |
| `AUTH_TOKEN_INVALID`            | 401  | Token signature/claims invalid                |
| `AUTH_INSUFFICIENT_PERMISSIONS` | 403  | Membership role too low for action            |
| `VALIDATION_ERROR`              | 422  | Request body failed validation                |
| `RESOURCE_NOT_FOUND`            | 404  | Requested resource does not exist             |
| `RESOURCE_CONFLICT`             | 409  | Slug already taken, version mismatch          |
| `STATE_TRANSITION_INVALID`      | 409  | Invalid status change (e.g., done → todo)     |
| `RATE_LIMIT_EXCEEDED`           | 429  | Too many requests; check Retry-After header   |
| `INTERNAL_ERROR`                | 500  | Unexpected server error                       |
| `SERVICE_UNAVAILABLE`           | 503  | Planned or unplanned downtime                 |
| `REQUEST_TOO_LARGE`             | 400  | Payload exceeds `max_request_size`            |

### 4.5 Rate Limiting

Rate limits are communicated via standard headers:

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 987
X-RateLimit-Reset: 1719357300
Retry-After: 42
```

Limits are scoped per authenticated user. Unauthenticated endpoints have stricter limits.

| Tier      | Requests / Minute |
|-----------|-------------------|
| Default   | 60                |
| Authenticated | 1,000         |
| Admin     | 5,000             |

---

## 5. Endpoint Definitions

### 5.1 Resource URL Convention

```
/v1/{resource}              — List / Create
/v1/{resource}/{id}         — Get / Update / Delete
/v1/{resource}/{id}/{action} — Custom action
/v1/{resource}/{id}/{subresource} — Sub-resource operations
```

All IDs use prefixed opaque strings: `usr_`, `team_`, `prj_`, `tsk_`, `cmt_`, `tag_`, `att_`.

### 5.2 Users

| Method   | Path              | Description              | Status Codes        |
|----------|-------------------|--------------------------|---------------------|
| `GET`    | `/users`          | List users (team-scoped) | 200                  |
| `GET`    | `/users/{id}`     | Get user profile         | 200, 404             |
| `PATCH`  | `/users/{id}`     | Update own profile       | 200, 403, 404, 422   |
| `DELETE` | `/users/{id}`     | Deactivate account       | 204, 403, 404        |
| `GET`    | `/users/{id}/tasks` | Tasks assigned to user | 200, 404             |

### 5.3 Teams

| Method   | Path                          | Description                     | Status Codes           |
|----------|-------------------------------|---------------------------------|------------------------|
| `GET`    | `/teams`                      | List current user's teams       | 200                     |
| `POST`   | `/teams`                      | Create team                     | 201, 400, 422           |
| `GET`    | `/teams/{id}`                 | Get team details                | 200, 403, 404           |
| `PATCH`  | `/teams/{id}`                 | Update team                     | 200, 403, 404, 422      |
| `DELETE` | `/teams/{id}`                 | Delete team                     | 204, 403, 404, 409      |
| `GET`    | `/teams/{id}/members`         | List members                    | 200, 403, 404           |
| `POST`   | `/teams/{id}/members`         | Add member (invite)             | 201, 403, 404, 409, 422 |
| `PATCH`  | `/teams/{id}/members/{uid}`   | Change member role              | 200, 403, 404, 422      |
| `DELETE` | `/teams/{id}/members/{uid}`   | Remove member                   | 204, 403, 404, 409      |
| `GET`    | `/teams/{id}/projects`        | List team projects              | 200, 403, 404           |

### 5.4 Projects

| Method   | Path                            | Description                  | Status Codes         |
|----------|---------------------------------|------------------------------|----------------------|
| `GET`    | `/projects`                     | List accessible projects     | 200                   |
| `POST`   | `/projects`                     | Create project               | 201, 400, 403, 422    |
| `GET`    | `/projects/{id}`                | Get project details          | 200, 403, 404         |
| `PUT`    | `/projects/{id}`                | Full update project          | 200, 403, 404, 422    |
| `PATCH`  | `/projects/{id}`                | Partial update project       | 200, 403, 404, 422    |
| `DELETE` | `/projects/{id}`                | Archive project (soft delete)| 204, 403, 404, 409    |
| `POST`   | `/projects/{id}/archive`        | Explicitly archive           | 200, 403, 404, 409    |
| `POST`   | `/projects/{id}/restore`        | Restore from archive         | 200, 403, 404, 409    |
| `GET`    | `/projects/{id}/tasks`          | List project tasks           | 200, 403, 404         |
| `GET`    | `/projects/{id}/statistics`     | Project-level stats          | 200, 403, 404         |

### 5.5 Tasks

| Method   | Path                                | Description                   | Status Codes         |
|----------|-------------------------------------|-------------------------------|----------------------|
| `GET`    | `/tasks`                            | List tasks (filterable)       | 200                   |
| `POST`   | `/tasks`                            | Create task                   | 201, 400, 403, 422    |
| `GET`    | `/tasks/{id}`                       | Get task details              | 200, 403, 404         |
| `PUT`    | `/tasks/{id}`                       | Full update task              | 200, 403, 404, 422    |
| `PATCH`  | `/tasks/{id}`                       | Partial update task           | 200, 403, 404, 422    |
| `DELETE` | `/tasks/{id}`                       | Delete task                   | 204, 403, 404, 409    |
| `GET`    | `/tasks/{id}/subtasks`              | List child tasks              | 200, 403, 404         |
| `GET`    | `/tasks/{id}/comments`              | List comments                 | 200, 403, 404         |
| `POST`   | `/tasks/{id}/comments`              | Add comment                   | 201, 400, 403, 404    |
| `POST`   | `/tasks/{id}/attachments`           | Upload attachment             | 201, 400, 403, 404    |
| `GET`    | `/tasks/{id}/activity`              | View activity log             | 200, 403, 404         |

### 5.6 Comments

| Method   | Path                     | Description         | Status Codes         |
|----------|--------------------------|---------------------|----------------------|
| `PATCH`  | `/comments/{id}`         | Edit comment        | 200, 403, 404, 422   |
| `DELETE` | `/comments/{id}`         | Delete comment      | 204, 403, 404        |

### 5.7 Tags

| Method   | Path                          | Description              | Status Codes         |
|----------|-------------------------------|--------------------------|----------------------|
| `GET`    | `/teams/{id}/tags`            | List team tags           | 200, 403, 404         |
| `POST`   | `/teams/{id}/tags`            | Create tag               | 201, 403, 404, 422    |
| `PATCH`  | `/tags/{id}`                  | Update tag               | 200, 403, 404, 422    |
| `DELETE` | `/tags/{id}`                  | Delete tag               | 204, 403, 404         |
| `PUT`    | `/tasks/{id}/tags`            | Set tags on task         | 200, 403, 404         |
| `PUT`    | `/projects/{id}/tags`         | Set tags on project      | 200, 403, 404         |

### 5.8 Attachments

| Method   | Path                       | Description               | Status Codes         |
|----------|----------------------------|---------------------------|----------------------|
| `GET`    | `/attachments/{id}`        | Get attachment metadata   | 200, 403, 404         |
| `GET`    | `/attachments/{id}/download` | Download file           | 200, 403, 404         |
| `DELETE` | `/attachments/{id}`        | Delete attachment         | 204, 403, 404         |

### 5.9 Search

| Method | Path         | Description                      | Status Codes |
|--------|--------------|----------------------------------|--------------|
| `GET`  | `/search`    | Full-text search across resources | 200           |

Query parameters: `q` (search term), `scope` (projects|tasks|comments|all), `team_id`.

### 5.10 Webhooks (Admin)

| Method   | Path                          | Description        | Status Codes         |
|----------|-------------------------------|--------------------|----------------------|
| `GET`    | `/teams/{id}/webhooks`        | List webhooks      | 200, 403, 404         |
| `POST`   | `/teams/{id}/webhooks`        | Create webhook     | 201, 403, 404, 422    |
| `PATCH`  | `/webhooks/{id}`              | Update webhook     | 200, 403, 404, 422    |
| `DELETE` | `/webhooks/{id}`              | Delete webhook     | 204, 403, 404         |

---

## 6. Request/Response Schemas

### 6.1 Auth Schemas

#### POST /auth/register — Request

```json
{
  "email": "alice@example.com",
  "password": "S3cure!Pass",
  "name": "Alice Johnson"
}
```

| Field      | Type   | Constraints                          |
|------------|--------|--------------------------------------|
| `email`    | string | Valid email, unique, max 255 chars   |
| `password` | string | Min 8 chars, 1 upper, 1 lower, 1 digit |
| `name`     | string | Min 1 char, max 100 chars            |

#### POST /auth/register — Response (201)

```json
{
  "user": {
    "id": "usr_a1b2c3d4",
    "email": "alice@example.com",
    "name": "Alice Johnson",
    "avatar_url": null,
    "role": "user",
    "created_at": "2026-06-25T12:00:00Z",
    "updated_at": "2026-06-25T12:00:00Z"
  },
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "refresh_token": "dGhpcyBpcyBhIHJlZnJl...",
  "expires_in": 900,
  "token_type": "Bearer"
}
```

#### POST /auth/login — Request

```json
{
  "email": "alice@example.com",
  "password": "S3cure!Pass"
}
```

#### POST /auth/login — Response (200)

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "refresh_token": "dGhpcyBpcyBhIHJlZnJl...",
  "expires_in": 900,
  "token_type": "Bearer"
}
```

#### POST /auth/refresh — Request

```json
{
  "refresh_token": "dGhpcyBpcyBhIHJlZnJl..."
}
```

#### POST /auth/refresh — Response (200)

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "refresh_token": "bmV3IHJlZnJlc2ggdG9r...",
  "expires_in": 900,
  "token_type": "Bearer"
}
```

### 6.2 User Schemas

#### User Object

```json
{
  "id": "usr_a1b2c3d4",
  "email": "alice@example.com",
  "name": "Alice Johnson",
  "avatar_url": "https://cdn.promgr.example.com/avatars/usr_a1b2c3d4.jpg",
  "role": "user",
  "timezone": "America/Chicago",
  "created_at": "2026-06-25T12:00:00Z",
  "updated_at": "2026-06-25T12:00:00Z"
}
```

#### PATCH /users/{id} — Request

```json
{
  "name": "Alice Johnson-Smith",
  "timezone": "America/New_York"
}
```

All fields optional. Only `name`, `timezone`, and `avatar_url` are patchable by the user themselves.

### 6.3 Team Schemas

#### Team Object

```json
{
  "id": "team_x9y8z7w6",
  "name": "Engineering",
  "slug": "engineering",
  "description": "Core engineering team",
  "owner_id": "usr_a1b2c3d4",
  "member_count": 12,
  "my_role": "admin",
  "created_at": "2026-06-01T08:00:00Z",
  "updated_at": "2026-06-20T14:30:00Z"
}
```

#### POST /teams — Request

```json
{
  "name": "Engineering",
  "description": "Core engineering team"
}
```

| Field         | Type   | Constraints               |
|---------------|--------|----------------------------|
| `name`        | string | Required, 1-100 chars      |
| `description` | string | Optional, max 500 chars    |

#### POST /teams — Response (201)

```json
{
  "id": "team_x9y8z7w6",
  "name": "Engineering",
  "slug": "engineering",
  "description": "Core engineering team",
  "owner_id": "usr_a1b2c3d4",
  "member_count": 1,
  "my_role": "owner",
  "created_at": "2026-06-25T12:00:00Z",
  "updated_at": "2026-06-25T12:00:00Z"
}
```

#### Membership Object

```json
{
  "user": {
    "id": "usr_a1b2c3d4",
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "avatar_url": null
  },
  "role": "admin",
  "joined_at": "2026-06-01T08:00:00Z"
}
```

#### POST /teams/{id}/members — Request

```json
{
  "email": "bob@example.com",
  "role": "member"
}
```

| Field   | Type   | Constraints                                           |
|---------|--------|--------------------------------------------------------|
| `email` | string | Required, must be an existing user                    |
| `role`  | string | Required, one of: `admin`, `member`, `viewer`         |

### 6.4 Project Schemas

#### Project Object

```json
{
  "id": "prj_p1q2r3s4",
  "name": "Mobile App Redesign",
  "slug": "mobile-app-redesign",
  "description": "Complete overhaul of the mobile UI",
  "team_id": "team_x9y8z7w6",
  "status": "active",
  "start_date": "2026-07-01",
  "due_date": "2026-09-30",
  "owner_id": "usr_a1b2c3d4",
  "task_count": {
    "total": 45,
    "done": 12,
    "in_progress": 18
  },
  "tags": ["tag_q1w2", "tag_e3r4"],
  "created_at": "2026-06-25T12:00:00Z",
  "updated_at": "2026-06-25T12:00:00Z"
}
```

#### POST /projects — Request

```json
{
  "team_id": "team_x9y8z7w6",
  "name": "Mobile App Redesign",
  "description": "Complete overhaul of the mobile UI",
  "start_date": "2026-07-01",
  "due_date": "2026-09-30"
}
```

| Field         | Type    | Constraints                    |
|---------------|---------|--------------------------------|
| `team_id`     | string  | Required, must exist & user must be member |
| `name`        | string  | Required, 1-200 chars          |
| `description` | string  | Optional, max 2000 chars       |
| `start_date`  | string  | Optional, ISO 8601 date        |
| `due_date`    | string  | Optional, ISO 8601 date, must be >= start_date |

#### PATCH /projects/{id} — Request

```json
{
  "status": "on_hold",
  "due_date": "2026-10-15"
}
```

All top-level writable fields are optional. Status transitions are validated:

```
Valid transitions:
  active    → on_hold, completed, archived
  on_hold   → active, archived
  completed → active, archived
  archived  → active (only if not completed)
```

### 6.5 Task Schemas

#### Task Object

```json
{
  "id": "tsk_t1u2v3w4",
  "title": "Implement login screen",
  "description": "Build the login screen with email/password and SSO options.",
  "project_id": "prj_p1q2r3s4",
  "assignee_id": "usr_a1b2c3d4",
  "parent_task_id": null,
  "status": "in_progress",
  "priority": "high",
  "estimated_hours": 8.0,
  "actual_hours": 3.5,
  "due_date": "2026-07-15",
  "order": 2,
  "subtask_count": 3,
  "comment_count": 7,
  "tags": ["tag_frontend", "tag_sprint-4"],
  "created_at": "2026-06-25T12:00:00Z",
  "updated_at": "2026-06-25T12:00:00Z"
}
```

#### POST /tasks — Request

```json
{
  "project_id": "prj_p1q2r3s4",
  "title": "Implement login screen",
  "description": "Build the login screen with email/password and SSO options.",
  "assignee_id": "usr_a1b2c3d4",
  "parent_task_id": null,
  "priority": "high",
  "estimated_hours": 8.0,
  "due_date": "2026-07-15",
  "order": 2
}
```

| Field            | Type    | Constraints                                    |
|------------------|---------|------------------------------------------------|
| `project_id`     | string  | Required, must exist                           |
| `title`          | string  | Required, 1-500 chars                          |
| `description`    | string  | Optional, max 10000 chars (Markdown supported) |
| `assignee_id`    | string  | Optional, must be team member                  |
| `parent_task_id` | string  | Optional, must exist in same project           |
| `priority`       | string  | Optional, defaults to `medium`                 |
| `estimated_hours`| number  | Optional, non-negative                         |
| `due_date`       | string  | Optional, ISO 8601 date                        |
| `order`          | number  | Optional, float for flexible reordering        |

#### PATCH /tasks/{id} — Request (Status-only update example)

```json
{
  "status": "in_review"
}
```

Status transitions are validated:

```
task_status_transitions:
  backlog     → todo
  todo        → in_progress, cancelled
  in_progress → in_review, todo, cancelled
  in_review   → done, in_progress
  done        → in_progress
  cancelled   → todo
```

#### PUT /tasks/{id}/tags — Request

```json
{
  "tag_ids": ["tag_frontend", "tag_sprint-4", "tag_urgent"]
}
```

Replaces the entire set of tags on the task.

### 6.6 Comment Schemas

#### Comment Object

```json
{
  "id": "cmt_c1d2e3f4",
  "task_id": "tsk_t1u2v3w4",
  "author": {
    "id": "usr_a1b2c3d4",
    "name": "Alice Johnson",
    "avatar_url": null
  },
  "body": "I've started working on the form validation. Will push a PR by EOD.",
  "body_html": "<p>I've started working on the form validation. Will push a PR by EOD.</p>",
  "created_at": "2026-06-25T14:30:00Z",
  "updated_at": "2026-06-25T14:30:00Z"
}
```

#### POST /tasks/{id}/comments — Request

```json
{
  "body": "I've started working on the form validation."
}
```

| Field  | Type   | Constraints          |
|--------|--------|----------------------|
| `body` | string | Required, 1-5000 chars (Markdown) |

### 6.7 Tag Schemas

#### Tag Object

```json
{
  "id": "tag_frontend",
  "name": "Frontend",
  "color": "#3B82F6",
  "team_id": "team_x9y8z7w6",
  "created_at": "2026-06-25T12:00:00Z"
}
```

#### POST /teams/{id}/tags — Request

```json
{
  "name": "Frontend",
  "color": "#3B82F6"
}
```

| Field   | Type   | Constraints                       |
|---------|--------|-----------------------------------|
| `name`  | string | Required, 1-50 chars, unique      |
| `color` | string | Optional, hex color code          |

### 6.8 Attachment Schemas

#### Attachment Object

```json
{
  "id": "att_f5g6h7i8",
  "task_id": "tsk_t1u2v3w4",
  "filename": "login-mockup.png",
  "content_type": "image/png",
  "size_bytes": 245760,
  "uploaded_by": {
    "id": "usr_a1b2c3d4",
    "name": "Alice Johnson"
  },
  "url": "https://cdn.promgr.example.com/attachments/att_f5g6h7i8/login-mockup.png",
  "created_at": "2026-06-25T12:00:00Z"
}
```

#### POST /tasks/{id}/attachments — Request

Multipart form upload:

```
Content-Type: multipart/form-data

file: <binary>
```

Constraints: Max 50 MB per file. Supported types: images, PDFs, Office documents, text files.

### 6.9 Statistics Schema

#### GET /projects/{id}/statistics — Response (200)

```json
{
  "project_id": "prj_p1q2r3s4",
  "task_breakdown": {
    "total": 45,
    "backlog": 5,
    "todo": 10,
    "in_progress": 18,
    "in_review": 6,
    "done": 4,
    "cancelled": 2
  },
  "priority_breakdown": {
    "critical": 3,
    "high": 12,
    "medium": 22,
    "low": 8
  },
  "progress_percentage": 8.9,
  "estimated_hours_total": 320.0,
  "actual_hours_total": 45.5,
  "overdue_tasks": 3,
  "avg_cycle_time_days": 4.2
}
```

### 6.10 Search Schema

#### GET /search — Response (200)

```json
{
  "query": "login redesign",
  "results": [
    {
      "type": "task",
      "id": "tsk_t1u2v3w4",
      "title": "Implement login screen",
      "project_name": "Mobile App Redesign",
      "status": "in_progress",
      "highlight": "Build the <em>login</em> screen with email/password and SSO options.",
      "relevance_score": 0.92
    },
    {
      "type": "project",
      "id": "prj_p1q2r3s4",
      "name": "Mobile App Redesign",
      "status": "active",
      "highlight": "Complete overhaul of the mobile UI including <em>login</em> flow <em>redesign</em>.",
      "relevance_score": 0.87
    }
  ],
  "pagination": {
    "next_cursor": "eyJ0eXBlIjoidGFzayIsImlkIjoiLi4uIn0=",
    "prev_cursor": null,
    "has_next": false,
    "has_prev": false,
    "total_count": 2,
    "limit": 25
  }
}
```

---

## 7. OpenAPI 3.0 Specification

```yaml
openapi: 3.0.3
info:
  title: Project Management SaaS API
  description: |
    REST API for a multi-tenant project management platform.
    Manage projects, tasks, users, and teams with full CRUD operations.

    ## Authentication
    All authenticated endpoints require a JWT Bearer token in the
    `Authorization` header: `Authorization: Bearer <access_token>`.

    Obtain tokens via `POST /auth/login` or `POST /auth/register`.
    Refresh expired access tokens with `POST /auth/refresh`.

    ## Pagination
    List endpoints use cursor-based pagination. Include `cursor` from
    the previous response's `pagination.next_cursor` to fetch the next page.

    ## Rate Limiting
    Authenticated users: 1,000 requests per minute.
    Rate limit status is returned in `X-RateLimit-*` headers.

    ## Errors
    All errors follow a consistent format with `code`, `message`, and
    `request_id` fields. See the Error schema for details.
  version: 1.0.0
  contact:
    name: API Support
    email: api-support@promgr.example.com
  license:
    name: Proprietary

servers:
  - url: https://api.promgr.example.com/v1
    description: Production
  - url: https://api-staging.promgr.example.com/v1
    description: Staging

tags:
  - name: Auth
    description: Authentication and token management
  - name: Users
    description: User profile management
  - name: Teams
    description: Team and membership management
  - name: Projects
    description: Project lifecycle management
  - name: Tasks
    description: Task CRUD and workflow
  - name: Comments
    description: Task discussion threads
  - name: Tags
    description: Labeling and categorization
  - name: Attachments
    description: File uploads and downloads
  - name: Search
    description: Full-text search across resources
  - name: Webhooks
    description: Outbound event notifications

# ── Security ─────────────────────────────────────────────────

security:
  - BearerAuth: []

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: |
        JWT access token obtained from POST /auth/login or POST /auth/register.

  # ── Schemas ────────────────────────────────────────────────

  schemas:
    # --- Common ---
    Error:
      type: object
      required: [code, message, request_id]
      properties:
        code:
          type: string
          description: Machine-readable error code
          example: "VALIDATION_ERROR"
        message:
          type: string
          description: Human-readable error message
          example: "One or more fields failed validation."
        request_id:
          type: string
          description: Unique request identifier for tracing
          example: "req_9f8e7d6c5b4a"
        details:
          type: array
          items:
            $ref: '#/components/schemas/ErrorDetail'

    ErrorDetail:
      type: object
      properties:
        field:
          type: string
          example: "email"
        code:
          type: string
          example: "INVALID_FORMAT"
        message:
          type: string
          example: "Must be a valid email address."

    Pagination:
      type: object
      properties:
        next_cursor:
          type: string
          nullable: true
          example: "eyJpZCI6InByal84ODgifQ=="
        prev_cursor:
          type: string
          nullable: true
        has_next:
          type: boolean
        has_prev:
          type: boolean
        total_count:
          type: integer
          example: 142
        limit:
          type: integer
          example: 25

    # --- Auth ---
    LoginRequest:
      type: object
      required: [email, password]
      properties:
        email:
          type: string
          format: email
          example: "alice@example.com"
        password:
          type: string
          format: password
          minLength: 8
          example: "S3cure!Pass"

    RegisterRequest:
      type: object
      required: [email, password, name]
      properties:
        email:
          type: string
          format: email
        password:
          type: string
          format: password
          minLength: 8
        name:
          type: string
          minLength: 1
          maxLength: 100

    TokenResponse:
      type: object
      properties:
        access_token:
          type: string
          description: JWT access token (15-minute lifetime)
        refresh_token:
          type: string
          description: Opaque refresh token (14-day lifetime)
        expires_in:
          type: integer
          description: Seconds until access token expires
          example: 900
        token_type:
          type: string
          enum: [Bearer]
          example: "Bearer"

    AuthResponse:
      allOf:
        - $ref: '#/components/schemas/TokenResponse'
        - type: object
          properties:
            user:
              $ref: '#/components/schemas/User'

    RefreshRequest:
      type: object
      required: [refresh_token]
      properties:
        refresh_token:
          type: string

    # --- User ---
    User:
      type: object
      properties:
        id:
          type: string
          example: "usr_a1b2c3d4"
        email:
          type: string
          format: email
        name:
          type: string
        avatar_url:
          type: string
          format: uri
          nullable: true
        role:
          type: string
          enum: [super_admin, user]
        timezone:
          type: string
          example: "America/Chicago"
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    UserUpdate:
      type: object
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 100
        timezone:
          type: string
        avatar_url:
          type: string
          format: uri

    # --- Team ---
    Team:
      type: object
      properties:
        id:
          type: string
          example: "team_x9y8z7w6"
        name:
          type: string
        slug:
          type: string
        description:
          type: string
          nullable: true
        owner_id:
          type: string
        member_count:
          type: integer
        my_role:
          type: string
          enum: [owner, admin, member, viewer]
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    TeamCreate:
      type: object
      required: [name]
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 100
        description:
          type: string
          maxLength: 500

    TeamUpdate:
      type: object
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 100
        description:
          type: string
          maxLength: 500

    # --- Membership ---
    Membership:
      type: object
      properties:
        user:
          $ref: '#/components/schemas/UserSummary'
        role:
          type: string
          enum: [admin, member, viewer]
        joined_at:
          type: string
          format: date-time

    UserSummary:
      type: object
      properties:
        id:
          type: string
        name:
          type: string
        email:
          type: string
          format: email
        avatar_url:
          type: string
          nullable: true

    AddMemberRequest:
      type: object
      required: [email, role]
      properties:
        email:
          type: string
          format: email
        role:
          type: string
          enum: [admin, member, viewer]

    UpdateMemberRoleRequest:
      type: object
      required: [role]
      properties:
        role:
          type: string
          enum: [admin, member, viewer]

    # --- Project ---
    Project:
      type: object
      properties:
        id:
          type: string
          example: "prj_p1q2r3s4"
        name:
          type: string
        slug:
          type: string
        description:
          type: string
          nullable: true
        team_id:
          type: string
        status:
          type: string
          enum: [active, archived, completed, on_hold]
        start_date:
          type: string
          format: date
          nullable: true
        due_date:
          type: string
          format: date
          nullable: true
        owner_id:
          type: string
        task_count:
          type: object
          properties:
            total:
              type: integer
            done:
              type: integer
            in_progress:
              type: integer
        tags:
          type: array
          items:
            type: string
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    ProjectCreate:
      type: object
      required: [team_id, name]
      properties:
        team_id:
          type: string
        name:
          type: string
          minLength: 1
          maxLength: 200
        description:
          type: string
          maxLength: 2000
        start_date:
          type: string
          format: date
        due_date:
          type: string
          format: date

    ProjectUpdate:
      type: object
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 200
        description:
          type: string
          maxLength: 2000
        status:
          type: string
          enum: [active, archived, completed, on_hold]
        start_date:
          type: string
          format: date
        due_date:
          type: string
          format: date

    # --- Task ---
    Task:
      type: object
      properties:
        id:
          type: string
          example: "tsk_t1u2v3w4"
        title:
          type: string
        description:
          type: string
          nullable: true
        project_id:
          type: string
        assignee_id:
          type: string
          nullable: true
        parent_task_id:
          type: string
          nullable: true
        status:
          type: string
          enum: [backlog, todo, in_progress, in_review, done, cancelled]
        priority:
          type: string
          enum: [critical, high, medium, low]
        estimated_hours:
          type: number
          nullable: true
        actual_hours:
          type: number
          nullable: true
        due_date:
          type: string
          format: date
          nullable: true
        order:
          type: number
        subtask_count:
          type: integer
        comment_count:
          type: integer
        tags:
          type: array
          items:
            type: string
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    TaskCreate:
      type: object
      required: [project_id, title]
      properties:
        project_id:
          type: string
        title:
          type: string
          minLength: 1
          maxLength: 500
        description:
          type: string
          maxLength: 10000
        assignee_id:
          type: string
        parent_task_id:
          type: string
        priority:
          type: string
          enum: [critical, high, medium, low]
          default: medium
        estimated_hours:
          type: number
          minimum: 0
        due_date:
          type: string
          format: date
        order:
          type: number

    TaskUpdate:
      type: object
      properties:
        title:
          type: string
          minLength: 1
          maxLength: 500
        description:
          type: string
          maxLength: 10000
        assignee_id:
          type: string
          nullable: true
        status:
          type: string
          enum: [backlog, todo, in_progress, in_review, done, cancelled]
        priority:
          type: string
          enum: [critical, high, medium, low]
        estimated_hours:
          type: number
          minimum: 0
        actual_hours:
          type: number
          minimum: 0
        due_date:
          type: string
          format: date
        order:
          type: number

    SetTagsRequest:
      type: object
      required: [tag_ids]
      properties:
        tag_ids:
          type: array
          items:
            type: string
          uniqueItems: true

    # --- Comment ---
    Comment:
      type: object
      properties:
        id:
          type: string
          example: "cmt_c1d2e3f4"
        task_id:
          type: string
        author:
          $ref: '#/components/schemas/UserSummary'
        body:
          type: string
          description: Raw Markdown
        body_html:
          type: string
          description: Rendered HTML
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time

    CommentCreate:
      type: object
      required: [body]
      properties:
        body:
          type: string
          minLength: 1
          maxLength: 5000

    CommentUpdate:
      type: object
      required: [body]
      properties:
        body:
          type: string
          minLength: 1
          maxLength: 5000

    # --- Tag ---
    Tag:
      type: object
      properties:
        id:
          type: string
        name:
          type: string
        color:
          type: string
          pattern: '^#[0-9A-Fa-f]{6}$'
        team_id:
          type: string
        created_at:
          type: string
          format: date-time

    TagCreate:
      type: object
      required: [name]
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 50
        color:
          type: string
          pattern: '^#[0-9A-Fa-f]{6}$'

    TagUpdate:
      type: object
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 50
        color:
          type: string
          pattern: '^#[0-9A-Fa-f]{6}$'

    # --- Attachment ---
    Attachment:
      type: object
      properties:
        id:
          type: string
        task_id:
          type: string
        filename:
          type: string
        content_type:
          type: string
        size_bytes:
          type: integer
        uploaded_by:
          $ref: '#/components/schemas/UserSummary'
        url:
          type: string
          format: uri
        created_at:
          type: string
          format: date-time

    # --- Statistics ---
    ProjectStatistics:
      type: object
      properties:
        project_id:
          type: string
        task_breakdown:
          type: object
          properties:
            total: { type: integer }
            backlog: { type: integer }
            todo: { type: integer }
            in_progress: { type: integer }
            in_review: { type: integer }
            done: { type: integer }
            cancelled: { type: integer }
        priority_breakdown:
          type: object
          properties:
            critical: { type: integer }
            high: { type: integer }
            medium: { type: integer }
            low: { type: integer }
        progress_percentage:
          type: number
        estimated_hours_total:
          type: number
        actual_hours_total:
          type: number
        overdue_tasks:
          type: integer
        avg_cycle_time_days:
          type: number

    # --- Search ---
    SearchResult:
      type: object
      properties:
        type:
          type: string
          enum: [project, task, comment]
        id:
          type: string
        title:
          type: string
          description: Title for tasks/comments; name for projects
        project_name:
          type: string
          description: Only present for task and comment results
        status:
          type: string
        highlight:
          type: string
          description: Snippet with <em> highlighted matches
        relevance_score:
          type: number

    # --- Webhooks ---
    Webhook:
      type: object
      properties:
        id:
          type: string
        team_id:
          type: string
        url:
          type: string
          format: uri
        events:
          type: array
          items:
            type: string
            enum:
              - task.created
              - task.updated
              - task.deleted
              - task.status_changed
              - project.created
              - project.updated
              - comment.created
        secret:
          type: string
          description: HMAC signing secret (only returned on creation)
        active:
          type: boolean
        created_at:
          type: string
          format: date-time

    WebhookCreate:
      type: object
      required: [url, events]
      properties:
        url:
          type: string
          format: uri
        events:
          type: array
          items:
            type: string
            enum:
              - task.created
              - task.updated
              - task.deleted
              - task.status_changed
              - project.created
              - project.updated
              - comment.created
          minItems: 1
        active:
          type: boolean
          default: true

    WebhookUpdate:
      type: object
      properties:
        url:
          type: string
          format: uri
        events:
          type: array
          items:
            type: string
        active:
          type: boolean

    # --- List Envelopes ---
    UserList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'
        pagination:
          $ref: '#/components/schemas/Pagination'

    TeamList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/Team'
        pagination:
          $ref: '#/components/schemas/Pagination'

    MembershipList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/Membership'
        pagination:
          $ref: '#/components/schemas/Pagination'

    ProjectList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/Project'
        pagination:
          $ref: '#/components/schemas/Pagination'

    TaskList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/Task'
        pagination:
          $ref: '#/components/schemas/Pagination'

    CommentList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/Comment'
        pagination:
          $ref: '#/components/schemas/Pagination'

    TagList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/Tag'
        pagination:
          $ref: '#/components/schemas/Pagination'

    SearchResponse:
      type: object
      properties:
        query:
          type: string
        results:
          type: array
          items:
            $ref: '#/components/schemas/SearchResult'
        pagination:
          $ref: '#/components/schemas/Pagination'

    WebhookList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/Webhook'
        pagination:
          $ref: '#/components/schemas/Pagination'

  # ── Parameters ─────────────────────────────────────────────

  parameters:
    CursorParam:
      name: cursor
      in: query
      schema:
        type: string
      description: Opaque cursor from previous response's pagination.next_cursor

    LimitParam:
      name: limit
      in: query
      schema:
        type: integer
        minimum: 1
        maximum: 100
        default: 25

    SortParam:
      name: sort
      in: query
      schema:
        type: string
      description: "Sort field, prefix with '-' for descending (e.g., '-created_at')"

    TeamIdPath:
      name: team_id
      in: path
      required: true
      schema:
        type: string

    ProjectIdPath:
      name: project_id
      in: path
      required: true
      schema:
        type: string

    TaskIdPath:
      name: task_id
      in: path
      required: true
      schema:
        type: string

    UserIdPath:
      name: user_id
      in: path
      required: true
      schema:
        type: string

# ── Paths ────────────────────────────────────────────────────

paths:
  # ============================================================
  #  AUTH
  # ============================================================
  /auth/register:
    post:
      tags: [Auth]
      summary: Register a new user account
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RegisterRequest'
      responses:
        '201':
          description: User created, tokens returned
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AuthResponse'
        '409':
          description: Email already registered
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        '422':
          description: Validation error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

  /auth/login:
    post:
      tags: [Auth]
      summary: Authenticate and receive tokens
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/LoginRequest'
      responses:
        '200':
          description: Authentication successful
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TokenResponse'
        '401':
          description: Invalid credentials
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

  /auth/refresh:
    post:
      tags: [Auth]
      summary: Rotate access token using refresh token
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RefreshRequest'
      responses:
        '200':
          description: New token pair returned
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TokenResponse'
        '401':
          description: Invalid or expired refresh token
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

  /auth/logout:
    post:
      tags: [Auth]
      summary: Invalidate the current refresh token
      responses:
        '204':
          description: Successfully logged out
        '401':
          description: Invalid token

  /auth/forgot-password:
    post:
      tags: [Auth]
      summary: Send a password reset email
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [email]
              properties:
                email:
                  type: string
                  format: email
      responses:
        '200':
          description: Reset email sent (always 200 to prevent enumeration)
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: "If the email is registered, a reset link has been sent."

  /auth/reset-password:
    post:
      tags: [Auth]
      summary: Set a new password using a reset token
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [token, password]
              properties:
                token:
                  type: string
                password:
                  type: string
                  minLength: 8
      responses:
        '200':
          description: Password updated
        '422':
          description: Invalid or expired reset token

  /auth/me:
    get:
      tags: [Auth]
      summary: Get the current authenticated user's profile
      responses:
        '200':
          description: Current user profile
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '401':
          description: Not authenticated

  # ============================================================
  #  USERS
  # ============================================================
  /users:
    get:
      tags: [Users]
      summary: List users (filter by team membership)
      parameters:
        - name: team_id
          in: query
          schema:
            type: string
          description: Filter users by team membership
        - $ref: '#/components/parameters/CursorParam'
        - $ref: '#/components/parameters/LimitParam'
      responses:
        '200':
          description: Paginated list of users
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'

  /users/{user_id}:
    get:
      tags: [Users]
      summary: Get a user's public profile
      parameters:
        - $ref: '#/components/parameters/UserIdPath'
      responses:
        '200':
          description: User profile
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          description: User not found
    patch:
      tags: [Users]
      summary: Update the current user's profile
      parameters:
        - $ref: '#/components/parameters/UserIdPath'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserUpdate'
      responses:
        '200':
          description: Updated user profile
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '403':
          description: Cannot modify another user's profile
        '422':
          description: Validation error
    delete:
      tags: [Users]
      summary: Deactivate (soft-delete) a user account
      parameters:
        - $ref: '#/components/parameters/UserIdPath'
      responses:
        '204':
          description: Account deactivated
        '403':
          description: Not authorized

  /users/{user_id}/tasks:
    get:
      tags: [Users]
      summary: List tasks assigned to a user
      parameters:
        - $ref: '#/components/parameters/UserIdPath'
        - $ref: '#/components/parameters/CursorParam'
        - $ref: '#/components/parameters/LimitParam'
        - name: status
          in: query
          schema:
            type: string
            enum: [backlog, todo, in_progress, in_review, done, cancelled]
      responses:
        '200':
          description: Paginated task list
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TaskList'
        '404':
          description: User not found

  # ============================================================
  #  TEAMS
  # ============================================================
  /teams:
    get:
      tags: [Teams]
      summary: List teams the current user belongs to
      parameters:
        - $ref: '#/components/parameters/CursorParam'
        - $ref: '#/components/parameters/LimitParam'
      responses:
        '200':
          description: Paginated team list
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TeamList'
    post:
      tags: [Teams]
      summary: Create a new team
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TeamCreate'
      responses:
        '201':
          description: Team created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Team'
        '422':
          description: Validation error

  /teams/{team_id}:
    get:
      tags: [Teams]
      summary: Get team details
      parameters:
        - $ref: '#/components/parameters/TeamIdPath'
      responses:
        '200':
          description: Team details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Team'
        '403':
          description: Not a team member
        '404':
          description: Team not found
    patch:
      tags: [Teams]
      summary: Update team details
      parameters:
        - $ref: '#/components/parameters/TeamIdPath'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TeamUpdate'
      responses:
        '200':
          description: Updated team
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Team'
        '403':
          description: Must be team admin or owner
        '422':
          description: Validation error
    delete:
      tags: [Teams]
      summary: Delete a team (must have no active projects)
      parameters:
        - $ref: '#/components/parameters/TeamIdPath'
      responses:
        '204':
          description: Team deleted
        '403':
          description: Must be team owner
        '409':
          description: Team has active projects

  /teams/{team_id}/members:
    get:
      tags: [Teams]
      summary: List team members
      parameters:
        - $ref: '#/components/parameters/TeamIdPath'
        - $ref: '#/components/parameters/CursorParam'
        - $ref: '#/components/parameters/LimitParam'
      responses:
        '200':
          description: Paginated member list
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MembershipList'
        '403':
          description: Not a team member
    post:
      tags: [Teams]
      summary: Add a member to the team
      parameters:
        - $ref: '#/components/parameters/TeamIdPath'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/AddMemberRequest'
      responses:
        '201':
          description: Member added
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Membership'
        '403':
          description: Must be team admin or owner
        '409':
          description: User is already a member

  /teams/{team_id}/members/{user_id}:
    patch:
      tags: [Teams]
      summary: Change a member's role
      parameters:
        - $ref: '#/components/parameters/TeamIdPath'
        - $ref: '#/components/parameters/UserIdPath'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateMemberRoleRequest'
      responses:
        '200':
          description: Role updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Membership'
        '403':
          description: Must be owner or admin (admin cannot modify owner)
        '404':
          description: Member not found
    delete:
      tags: [Teams]
      summary: Remove a member from the team
      parameters:
        - $ref: '#/components/parameters/TeamIdPath'
        - $ref: '#/components/parameters/UserIdPath'
      responses:
        '204':
          description: Member removed
        '403':
          description: Must be owner or admin
        '409':
          description: Cannot remove the owner

  /teams/{team_id}/projects:
    get:
      tags: [Teams]
      summary: List projects belonging to a team
      parameters:
        - $ref: '#/components/parameters/TeamIdPath'
        - $ref: '#/components/parameters/CursorParam'
        - $ref: '#/components/parameters/LimitParam'
        - name: status
          in: query
          schema:
            type: string
            enum: [active, archived, completed, on_hold]
      responses:
        '200':
          description: Paginated project list
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProjectList'
        '403':
          description: Not a team member

  # ============================================================
  #  PROJECTS
  # ============================================================
  /projects:
    get:
      tags: [Projects]
      summary: List all projects accessible to the current user
      parameters:
        - $ref: '#/components/parameters/CursorParam'
        - $ref: '#/components/parameters/LimitParam'
        - $ref: '#/components/parameters/SortParam'
        - name: team_id
          in: query
          schema:
            type: string
        - name: status
          in: query
          schema:
            type: string
            enum: [active, archived, completed, on_hold]
      responses:
        '200':
          description: Paginated project list
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProjectList'
    post:
      tags: [Projects]
      summary: Create a new project
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ProjectCreate'
      responses:
        '201':
          description: Project created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Project'
        '403':
          description: Not authorized in target team
        '422':
          description: Validation error

  /projects/{project_id}:
    get:
      tags: [Projects]
      summary: Get project details
      parameters:
        - $ref: '#/components/parameters/ProjectIdPath'
      responses:
        '200':
          description: Project details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Project'
        '403':
          description: Access denied
        '404':
          description: Project not found
    put:
      tags: [Projects]
      summary: Full update of a project
      parameters:
        - $ref: '#/components/parameters/ProjectIdPath'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ProjectUpdate'
      responses:
        '200':
          description: Project updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Project'
        '403':
          description: Not authorized
        '422':
          description: Validation or state transition error
    patch:
      tags: [Projects]
      summary: Partial update of a project
      parameters:
        - $ref: '#/components/parameters/ProjectIdPath'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ProjectUpdate'
      responses:
        '200':
          description: Project updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Project'
    delete:
      tags: [Projects]
      summary: Archive (soft-delete) a project
      parameters:
        - $ref: '#/components/parameters/ProjectIdPath'
      responses:
        '204':
          description: Project archived
        '403':
          description: Not authorized
        '409':
          description: Cannot archive (has incomplete tasks)

  /projects/{project_id}/archive:
    post:
      tags: [Projects]
      summary: Explicitly archive a project
      parameters:
        - $ref: '#/components/parameters/ProjectIdPath'
      responses:
        '200':
          description: Project archived
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Project'
        '403':
          description: Not authorized

  /projects/{project_id}/restore:
    post:
      tags: [Projects]
      summary: Restore an archived project
      parameters:
        - $ref: '#/components/parameters/ProjectIdPath'
      responses:
        '200':
          description: Project restored
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Project'
        '403':
          description: Not authorized

  /projects/{project_id}/tasks:
    get:
      tags: [Projects]
      summary: List tasks in a project
      parameters:
        - $ref: '#/components/parameters/ProjectIdPath'
        - $ref: '#/components/parameters/CursorParam'
        - $ref: '#/components/parameters/LimitParam'
        - $ref: '#/components/parameters/SortParam'
        - name: status
          in: query
          schema:
            type: string
            enum: [backlog, todo, in_progress, in_review, done, cancelled]
        - name: assignee_id
          in: query
          schema:
            type: string
        - name: priority
          in: query
          schema:
            type: string
            enum: [critical, high, medium, low]
        - name: tag_id
          in: query
          schema:
            type: string
      responses:
        '200':
          description: Paginated task list
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TaskList'
        '403':
          description: Access denied

  /projects/{project_id}/statistics:
    get:
      tags: [Projects]
      summary: Get project-level statistics
      parameters:
        - $ref: '#/components/parameters/ProjectIdPath'
      responses:
        '200':
          description: Project statistics
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ProjectStatistics'
        '403':
          description: Access denied

  /projects/{project_id}/tags:
    put:
      tags: [Projects]
      summary: Set tags on a project (replaces all existing)
      parameters:
        - $ref: '#/components/parameters/ProjectIdPath'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/SetTagsRequest'
      responses:
        '200':
          description: Tags updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Project'

  # ============================================================
  #  TASKS
  # ============================================================
  /tasks:
    get:
      tags: [Tasks]
      summary: List tasks across projects (with filters)
      parameters:
        - $ref: '#/components/parameters/CursorParam'
        - $ref: '#/components/parameters/LimitParam'
        - $ref: '#/components/parameters/SortParam'
        - name: project_id
          in: query
          schema:
            type: string
        - name: assignee_id
          in: query
          schema:
            type: string
        - name: status
          in: query
          schema:
            type: string
            enum: [backlog, todo, in_progress, in_review, done, cancelled]
        - name: priority
          in: query
          schema:
            type: string
            enum: [critical, high, medium, low]
        - name: due_before
          in: query
          schema:
            type: string
            format: date
        - name: due_after
          in: query
          schema:
            type: string
            format: date
        - name: tag_id
          in: query
          schema:
            type: string
      responses:
        '200':
          description: Paginated task list
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TaskList'
    post:
      tags: [Tasks]
      summary: Create a new task
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TaskCreate'
      responses:
        '201':
          description: Task created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '403':
          description: Not authorized in project's team
        '422':
          description: Validation error

  /tasks/{task_id}:
    get:
      tags: [Tasks]
      summary: Get task details
      parameters:
        - $ref: '#/components/parameters/TaskIdPath'
      responses:
        '200':
          description: Task details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '403':
          description: Access denied
        '404':
          description: Task not found
    put:
      tags: [Tasks]
      summary: Full update of a task
      parameters:
        - $ref: '#/components/parameters/TaskIdPath'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TaskUpdate'
      responses:
        '200':
          description: Task updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
        '403':
          description: Not authorized
        '409':
          description: Invalid state transition
        '422':
          description: Validation error
    patch:
      tags: [Tasks]
      summary: Partial update of a task
      parameters:
        - $ref: '#/components/parameters/TaskIdPath'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TaskUpdate'
      responses:
        '200':
          description: Task updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'
    delete:
      tags: [Tasks]
      summary: Delete a task
      parameters:
        - $ref: '#/components/parameters/TaskIdPath'
      responses:
        '204':
          description: Task deleted
        '403':
          description: Not authorized
        '409':
          description: Cannot delete task with active subtasks

  /tasks/{task_id}/subtasks:
    get:
      tags: [Tasks]
      summary: List child tasks (subtasks)
      parameters:
        - $ref: '#/components/parameters/TaskIdPath'
        - $ref: '#/components/parameters/CursorParam'
        - $ref: '#/components/parameters/LimitParam'
      responses:
        '200':
          description: Paginated subtask list
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TaskList'

  /tasks/{task_id}/comments:
    get:
      tags: [Comments]
      summary: List comments on a task
      parameters:
        - $ref: '#/components/parameters/TaskIdPath'
        - $ref: '#/components/parameters/CursorParam'
        - $ref: '#/components/parameters/LimitParam'
      responses:
        '200':
          description: Paginated comment list
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/CommentList'
    post:
      tags: [Comments]
      summary: Add a comment to a task
      parameters:
        - $ref: '#/components/parameters/TaskIdPath'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CommentCreate'
      responses:
        '201':
          description: Comment created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Comment'
        '403':
          description: Access denied

  /tasks/{task_id}/attachments:
    post:
      tags: [Attachments]
      summary: Upload a file attachment to a task
      parameters:
        - $ref: '#/components/parameters/TaskIdPath'
      requestBody:
        required: true
        content:
          multipart/form-data:
            schema:
              type: object
              required: [file]
              properties:
                file:
                  type: string
                  format: binary
                  description: File to upload (max 50 MB)
      responses:
        '201':
          description: File uploaded
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Attachment'
        '400':
          description: File too large or unsupported type
        '403':
          description: Access denied

  /tasks/{task_id}/activity:
    get:
      tags: [Tasks]
      summary: Get activity log for a task
      parameters:
        - $ref: '#/components/parameters/TaskIdPath'
        - $ref: '#/components/parameters/CursorParam'
        - $ref: '#/components/parameters/LimitParam'
      responses:
        '200':
          description: Activity log entries
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      type: object
                      properties:
                        id:
                          type: string
                        action:
                          type: string
                          example: "task.status_changed"
                        actor:
                          $ref: '#/components/schemas/UserSummary'
                        changes:
                          type: object
                        timestamp:
                          type: string
                          format: date-time
                  pagination:
                    $ref: '#/components/schemas/Pagination'

  /tasks/{task_id}/tags:
    put:
      tags: [Tasks]
      summary: Set tags on a task (replaces all existing)
      parameters:
        - $ref: '#/components/parameters/TaskIdPath'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/SetTagsRequest'
      responses:
        '200':
          description: Tags updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Task'

  # ============================================================
  #  COMMENTS
  # ============================================================
  /comments/{comment_id}:
    patch:
      tags: [Comments]
      summary: Edit a comment (author only)
      parameters:
        - name: comment_id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CommentUpdate'
      responses:
        '200':
          description: Comment updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Comment'
        '403':
          description: Not the comment author
        '404':
          description: Comment not found
    delete:
      tags: [Comments]
      summary: Delete a comment
      parameters:
        - name: comment_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '204':
          description: Comment deleted
        '403':
          description: Not authorized

  # ============================================================
  #  TAGS
  # ============================================================
  /teams/{team_id}/tags:
    get:
      tags: [Tags]
      summary: List tags for a team
      parameters:
        - $ref: '#/components/parameters/TeamIdPath'
        - $ref: '#/components/parameters/CursorParam'
        - $ref: '#/components/parameters/LimitParam'
      responses:
        '200':
          description: Paginated tag list
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TagList'
    post:
      tags: [Tags]
      summary: Create a new tag
      parameters:
        - $ref: '#/components/parameters/TeamIdPath'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TagCreate'
      responses:
        '201':
          description: Tag created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Tag'
        '403':
          description: Not authorized
        '409':
          description: Tag name already exists in team

  /tags/{tag_id}:
    patch:
      tags: [Tags]
      summary: Update a tag
      parameters:
        - name: tag_id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TagUpdate'
      responses:
        '200':
          description: Tag updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Tag'
        '403':
          description: Not authorized
    delete:
      tags: [Tags]
      summary: Delete a tag
      parameters:
        - name: tag_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '204':
          description: Tag deleted
        '403':
          description: Not authorized

  # ============================================================
  #  ATTACHMENTS
  # ============================================================
  /attachments/{attachment_id}:
    get:
      tags: [Attachments]
      summary: Get attachment metadata
      parameters:
        - name: attachment_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Attachment metadata
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Attachment'
        '403':
          description: Access denied
        '404':
          description: Attachment not found
    delete:
      tags: [Attachments]
      summary: Delete an attachment
      parameters:
        - name: attachment_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '204':
          description: Attachment deleted
        '403':
          description: Not authorized

  /attachments/{attachment_id}/download:
    get:
      tags: [Attachments]
      summary: Download an attachment file
      parameters:
        - name: attachment_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: File contents
          content:
            application/octet-stream:
              schema:
                type: string
                format: binary
        '403':
          description: Access denied

  # ============================================================
  #  SEARCH
  # ============================================================
  /search:
    get:
      tags: [Search]
      summary: Full-text search across resources
      parameters:
        - name: q
          in: query
          required: true
          schema:
            type: string
            minLength: 2
          description: Search query
        - name: scope
          in: query
          schema:
            type: string
            enum: [projects, tasks, comments, all]
            default: all
        - name: team_id
          in: query
          schema:
            type: string
          description: Limit search to a specific team
        - $ref: '#/components/parameters/CursorParam'
        - $ref: '#/components/parameters/LimitParam'
      responses:
        '200':
          description: Search results
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SearchResponse'
        '422':
          description: Query too short

  # ============================================================
  #  WEBHOOKS
  # ============================================================
  /teams/{team_id}/webhooks:
    get:
      tags: [Webhooks]
      summary: List webhooks for a team
      parameters:
        - $ref: '#/components/parameters/TeamIdPath'
        - $ref: '#/components/parameters/CursorParam'
        - $ref: '#/components/parameters/LimitParam'
      responses:
        '200':
          description: Paginated webhook list
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/WebhookList'
        '403':
          description: Must be team admin or owner
    post:
      tags: [Webhooks]
      summary: Create a new webhook
      parameters:
        - $ref: '#/components/parameters/TeamIdPath'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/WebhookCreate'
      responses:
        '201':
          description: Webhook created (secret returned)
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Webhook'
        '403':
          description: Must be team admin or owner

  /webhooks/{webhook_id}:
    patch:
      tags: [Webhooks]
      summary: Update a webhook
      parameters:
        - name: webhook_id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/WebhookUpdate'
      responses:
        '200':
          description: Webhook updated
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Webhook'
        '403':
          description: Not authorized
    delete:
      tags: [Webhooks]
      summary: Delete a webhook
      parameters:
        - name: webhook_id
          in: path
          required: true
          schema:
            type: string
      responses:
        '204':
          description: Webhook deleted
        '403':
          description: Not authorized
```

---

## Appendix A: Client SDK Pseudocode

```python
# Example: Paginated fetch of all tasks in a project
def fetch_all_tasks(project_id: str):
    tasks = []
    cursor = None

    while True:
        params = {"limit": 100}
        if cursor:
            params["cursor"] = cursor

        response = api.get(f"/v1/projects/{project_id}/tasks", params=params)
        page = response.json()

        tasks.extend(page["data"])

        if not page["pagination"]["has_next"]:
            break
        cursor = page["pagination"]["next_cursor"]

    return tasks


# Example: Token refresh on 401
def authenticated_request(method: str, path: str, **kwargs):
    response = api.request(method, path, **kwargs)
    if response.status_code == 401:
        tokens = api.post("/v1/auth/refresh",
                          json={"refresh_token": stored_refresh_token}).json()
        store_tokens(tokens)
        # Retry with new token
        api.headers["Authorization"] = f"Bearer {tokens['access_token']}"
        response = api.request(method, path, **kwargs)
    return response
```

## Appendix B: Webhook Payload Format

```json
{
  "event": "task.status_changed",
  "timestamp": "2026-06-25T14:30:00Z",
  "team_id": "team_x9y8z7w6",
  "data": {
    "task": {
      "id": "tsk_t1u2v3w4",
      "title": "Implement login screen",
      "old_status": "in_progress",
      "new_status": "in_review"
    },
    "actor": {
      "id": "usr_a1b2c3d4",
      "name": "Alice Johnson"
    }
  }
}
```

Webhook deliveries include an `X-Webhook-Signature` header (HMAC-SHA256 of the payload using the webhook secret) for verification.

## Appendix C: API Versioning Strategy

- **URI path versioning**: `/v1/`, `/v2/` — explicit and unambiguous
- **Deprecation policy**: Old versions supported for 12 months after new version release
- **Deprecation header**: `Sunset: Sat, 01 Jan 2027 00:00:00 GMT` on deprecated endpoints
- **Breaking changes**: Only introduced in new major versions
- **Non-breaking additions**: New fields, new endpoints, new optional parameters — safe to add to current version

---

*Document version: 1.0.0 | Generated: 2026-06-25T21:39:00Z*
