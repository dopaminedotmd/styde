Authentication schema for a multi-tenant SaaS backend (PostgreSQL):
accounts table
  id UUID PK default gen_random_uuid()
  name VARCHAR(255) NOT NULL
  slug VARCHAR(100) UNIQUE NOT NULL
  plan tier ENUM(free,starter,pro,enterprise)
  created_at TIMESTAMPTZ default now()
  updated_at TIMESTAMPTZ
users table
  id UUID PK
  account_id UUID FK -> accounts.id NOT NULL
  email VARCHAR(255) NOT NULL
  password_hash VARCHAR(255) NOT NULL
  role ENUM(owner,admin,member,viewer) default member
  is_active BOOLEAN default true
  last_login TIMESTAMPTZ
  created_at TIMESTAMPTZ default now()
Indexes:
  UNIQUE (email) WHERE is_active = true
  (account_id, role) for account-scoped user listing
  (last_login) for cleanup of dormant accounts
sessions table
  id UUID PK
  user_id UUID FK -> users.id NOT NULL
  token_hash VARCHAR(64) UNIQUE NOT NULL
  ip INET
  user_agent TEXT
  expires_at TIMESTAMPTZ NOT NULL
  created_at TIMESTAMPTZ default now()
Indexes:
  (token_hash) for fast auth lookup
  (user_id, expires_at) for session enumeration
  (expires_at) partial index WHERE expires_at < now() for TTL cleanup
audit_logs table (append-only)
  id BIGSERIAL PK
  account_id UUID FK -> accounts.id
  actor_id UUID FK -> users.id
  action VARCHAR(50) NOT NULL
  entity_type VARCHAR(50)
  entity_id UUID
  changes JSONB
  ip INET
  created_at TIMESTAMPTZ default now()
Index:
  (account_id, created_at DESC) for recent activity feed
  (entity_type, entity_id, created_at) for per-entity history
Migration v001: CREATE EXTENSION pgcrypto; CREATE TABLE accounts; CREATE TABLE users; CREATE TABLE sessions; CREATE TABLE audit_logs; CREATE INDEXES.
Migration v002 (reversible): ALTER TABLE users ADD COLUMN mfa_enabled BOOLEAN default false; ALTER TABLE sessions ADD COLUMN mfa_verified BOOLEAN default false.
Rationale for relational over document: strong referential integrity across accounts/users/sessions, transactional consistency for signup flows, partial unique indexes for soft-delete patterns, JSONB on audit_logs for flexible event shapes without schema rigidity.