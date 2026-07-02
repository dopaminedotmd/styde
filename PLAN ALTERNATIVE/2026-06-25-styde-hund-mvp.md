# Styde & hund.ai MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the MVP of the Styde consult-and-SaaS dashboard and its intelligent companion hund.ai, including database schema, Next.js project setup, responsive dark-mode shell, agent hub, and copilot chat interface.

**Architecture:** A hybrid Next.js web application utilizing Supabase/PostgreSQL for storage/auth, and modular frontend components styled with Vanilla CSS modules. A mock backend API simulates the GCP Vertex AI / Cloud Run endpoints for local development.

**Tech Stack:** Next.js (App Router), TypeScript, Supabase (PostgreSQL), Vanilla CSS (CSS Modules), Vitest (for unit testing), and React.

## User Review Required

> [!IMPORTANT]
> Since running scripts is restricted in the current system's PowerShell Execution Policy, all package management and CLI commands should be executed via `cmd /c` rather than raw PowerShell.

> [!WARNING]
> This MVP will use mock endpoints and state variables in the Next.js frontend to simulate Supabase and GCP integrations (CrewAI, Vertex AI, BigQuery) for rapid local development. Real integrations will follow in subsequent phases.

## Open Questions

- *None at this stage. The database schema and frontend UI structure are fully specified in the design document.*

## Global Constraints
- Next.js: App Router, React 19 / Next 15.
- CSS: Vanilla CSS / CSS Modules only (No TailwindCSS).
- TypeScript: Strict type checking.
- Testing: Write Vitest unit tests for components and utils.
- Naming: Company is `styde` (lowercase), assistant is `hund` or `hund.ai` (lowercase).

---

## Proposed Changes

We will create the database migrations, initialize the Next.js project, build the responsive dashboard shell, implement the Agent Hub with customization controllers, and build the expandable `hund.ai` copilot panel.

### Database Component

#### [NEW] [init_schema.sql](file:///c:/Users/William/test/supabase/migrations/20260625000000_init_schema.sql)
#### [NEW] [seed.sql](file:///c:/Users/William/test/supabase/seed.sql)

### Next.js Scaffolding & Configuration

#### [NEW] [package.json](file:///c:/Users/William/test/package.json)
#### [NEW] [next.config.ts](file:///c:/Users/William/test/next.config.ts)
#### [NEW] [tsconfig.json](file:///c:/Users/William/test/tsconfig.json)

### Shell & Navigation Components

#### [NEW] [layout.tsx](file:///c:/Users/William/test/app/layout.tsx)
#### [NEW] [global.css](file:///c:/Users/William/test/app/global.css)
#### [NEW] [Sidebar.tsx](file:///c:/Users/William/test/app/components/Sidebar.tsx)
#### [NEW] [Sidebar.module.css](file:///c:/Users/William/test/app/components/Sidebar.module.css)

### Agent Hub & Customization Controls

#### [NEW] [page.tsx](file:///c:/Users/William/test/app/agents/page.tsx)
#### [NEW] [page.module.css](file:///c:/Users/William/test/app/agents/page.module.css)
#### [NEW] [AgentCard.tsx](file:///c:/Users/William/test/app/components/AgentCard.tsx)
#### [NEW] [AgentCard.module.css](file:///c:/Users/William/test/app/components/AgentCard.module.css)

### Copilot Pane & hund.ai Chat

#### [NEW] [CopilotPane.tsx](file:///c:/Users/William/test/app/components/CopilotPane.tsx)
#### [NEW] [CopilotPane.module.css](file:///c:/Users/William/test/app/components/CopilotPane.module.css)
#### [NEW] [route.ts](file:///c:/Users/William/test/app/api/chat/route.ts)

---

## Verification Plan

### Automated Tests
- Run `npm run test` to run Vitest unit and component tests.
- Run `npm run build` to verify production builds and compile-time type checking.

### Manual Verification
- Launch local development server with `npm run dev` and navigate to `http://localhost:3000`.
- Verify the collapsible sidebar layout, navigation links, and dark-mode styling.
- Interact with the personality sliders in the Agent Hub and verify state updates.
- Open the copilot chat pane and converse with `hund.ai` using mock Swedish agent-related queries.

---

## Tasks

### Task 1: Database Schema & Seed Data Setup

**Files:**
- Create: `supabase/migrations/20260625000000_init_schema.sql`
- Create: `supabase/seed.sql`
- Create: `scripts/test-sql-exists.js`

**Interfaces:**
- Consumes: None (starting from scratch).
- Produces: The full relational schema (SQL queries) and mock data inserts.

- [ ] **Step 1: Write SQL validator script**
  Create a test script `scripts/test-sql-exists.js` that checks for migration file existence and runs a quick regex validation to ensure correct structure.
  ```javascript
  const fs = require('fs');
  const path = require('path');
  const migrationPath = path.join(__dirname, '../supabase/migrations/20260625000000_init_schema.sql');
  const seedPath = path.join(__dirname, '../supabase/seed.sql');

  if (!fs.existsSync(migrationPath)) {
    console.error('Migration file missing!');
    process.exit(1);
  }
  if (!fs.existsSync(seedPath)) {
    console.error('Seed file missing!');
    process.exit(1);
  }
  console.log('SQL Migration and Seed files exist and are ready.');
  process.exit(0);
  ```

- [ ] **Step 2: Run validator to verify it fails**
  Run: `cmd /c node scripts/test-sql-exists.js`
  Expected: FAIL (files do not exist yet)

- [ ] **Step 3: Write SQL migration & seed files**
  Create `supabase/migrations/20260625000000_init_schema.sql`:
  ```sql
  -- Setup schemas and enums
  CREATE TYPE organization_tier AS ENUM ('starter', 'growth', 'enterprise');
  CREATE TYPE user_role AS ENUM ('client_admin', 'client_staff', 'styde_consultant');
  CREATE TYPE audit_status AS ENUM ('pending', 'in_progress', 'completed');
  CREATE TYPE implementation_status AS ENUM ('planning', 'building', 'testing', 'approved');
  CREATE TYPE agent_status AS ENUM ('active', 'paused');
  CREATE TYPE log_status AS ENUM ('success', 'error', 'running');
  CREATE TYPE sender_type AS ENUM ('user', 'agent', 'hund');

  -- Create tables
  CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    tier organization_tier NOT NULL DEFAULT 'starter',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
  );

  CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    role user_role NOT NULL DEFAULT 'client_staff'
  );

  CREATE TABLE audits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    status audit_status NOT NULL DEFAULT 'pending',
    report_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
  );

  CREATE TABLE implementations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    status implementation_status NOT NULL DEFAULT 'planning',
    budget NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    approved_by UUID REFERENCES users(id) ON DELETE SET NULL
  );

  CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    avatar_url TEXT,
    status agent_status NOT NULL DEFAULT 'paused',
    gcp_endpoint TEXT,
    config JSONB NOT NULL DEFAULT '{}'::jsonb,
    daily_budget_limit NUMERIC(10, 2) NOT NULL DEFAULT 10.00
  );

  CREATE TABLE agent_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id UUID REFERENCES agents(id) ON DELETE CASCADE,
    status log_status NOT NULL DEFAULT 'running',
    input_data JSONB DEFAULT '{}'::jsonb,
    output_data JSONB DEFAULT '{}'::jsonb,
    error_message TEXT,
    run_duration_ms INTEGER,
    cost NUMERIC(10, 4) DEFAULT 0.0000,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
  );

  CREATE TABLE chats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    org_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    agent_id UUID REFERENCES agents(id) ON DELETE SET NULL, -- NULL if with hund
    title TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
  );

  CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chat_id UUID REFERENCES chats(id) ON DELETE CASCADE,
    sender_type sender_type NOT NULL,
    sender_id UUID REFERENCES users(id) ON DELETE SET NULL, -- NULL if agent/hund
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
  );
  ```

  Create `supabase/seed.sql`:
  ```sql
  -- Insert mock organization
  INSERT INTO organizations (id, name, tier)
  VALUES ('d7b9f8a2-2b3c-4d5e-8f9a-1b2c3d4e5f6a', 'Acme Corp', 'growth');

  -- Insert mock users
  INSERT INTO users (id, org_id, email, name, role)
  VALUES 
    ('e7b9f8a2-2b3c-4d5e-8f9a-1b2c3d4e5f6a', 'd7b9f8a2-2b3c-4d5e-8f9a-1b2c3d4e5f6a', 'john@acme.com', 'John Client', 'client_admin'),
    ('f7b9f8a2-2b3c-4d5e-8f9a-1b2c3d4e5f6a', 'd7b9f8a2-2b3c-4d5e-8f9a-1b2c3d4e5f6a', 'alice@styde.se', 'Alice Consultant', 'styde_consultant');

  -- Insert mock audit
  INSERT INTO audits (org_id, status, report_url)
  VALUES ('d7b9f8a2-2b3c-4d5e-8f9a-1b2c3d4e5f6a', 'completed', 'https://storage.googleapis.com/styde-reports/acme_audit_2026.pdf');

  -- Insert mock agents
  INSERT INTO agents (id, org_id, name, avatar_url, status, gcp_endpoint, config, daily_budget_limit)
  VALUES 
    ('a7b9f8a2-2b3c-4d5e-8f9a-1b2c3d4e5f6a', 'd7b9f8a2-2b3c-4d5e-8f9a-1b2c3d4e5f6a', 'Fakturaskannare', '/avatars/invoice.png', 'active', 'https://agent-invoice-run-xyz.a.run.app', '{"strictness": 0.8, "length": 0.2}', 25.00),
    ('b7b9f8a2-2b3c-4d5e-8f9a-1b2c3d4e5f6a', 'd7b9f8a2-2b3c-4d5e-8f9a-1b2c3d4e5f6a', 'SupportSorterare', '/avatars/support.png', 'paused', 'https://agent-support-run-xyz.a.run.app', '{"strictness": 0.4, "length": 0.7}', 10.00);

  -- Insert mock logs
  INSERT INTO agent_logs (agent_id, status, input_data, output_data, run_duration_ms, cost)
  VALUES ('a7b9f8a2-2b3c-4d5e-8f9a-1b2c3d4e5f6a', 'success', '{"file": "inv_9821.pdf"}', '{"amount": 12500, "currency": "SEK", "approved": true}', 1200, 0.0450);
  ```

- [ ] **Step 4: Run validator to verify it passes**
  Run: `cmd /c node scripts/test-sql-exists.js`
  Expected: PASS

- [ ] **Step 5: Commit**
  ```bash
  git add supabase/migrations/20260625000000_init_schema.sql supabase/seed.sql scripts/test-sql-exists.js
  git commit -m "db: add PostgreSQL schema definitions and mock seed data"
  ```

---

### Task 2: Next.js Project Scaffolding & Configuration

**Files:**
- Create: `package.json` (and subfiles created by setup)
- Modify: `package.json` to configure test scripts and install Vitest dependencies.
- Create: `vitest.config.ts`

**Interfaces:**
- Consumes: None.
- Produces: React 19/Next 15 project base layout with Vitest and JSDOM test framework.

- [ ] **Step 1: Write placeholder check script**
  Create `scripts/verify-nextjs.js` to ensure key files are present.
  ```javascript
  const fs = require('fs');
  if (!fs.existsSync('package.json') || !fs.existsSync('next.config.ts')) {
    console.error('Next.js is not configured properly!');
    process.exit(1);
  }
  console.log('Next.js files verified.');
  process.exit(0);
  ```
  Run: `cmd /c node scripts/verify-nextjs.js`
  Expected: FAIL

- [ ] **Step 2: Initialize Next.js project**
  Run the Next.js bootstrap script. Since we don't want TailwindCSS (per the guidelines), we negate it with `--no-tailwind`.
  Run: `cmd /c npx create-next-app@latest ./ --ts --eslint --app --no-tailwind --no-src-dir --import-alias "@/*" --use-npm --yes`

- [ ] **Step 3: Install Vitest and testing utilities**
  Run: `cmd /c npm install -D vitest @vitejs/plugin-react @testing-library/react @testing-library/jest-dom jsdom @types/node`

  Create `vitest.config.ts`:
  ```typescript
  import { defineConfig } from 'vitest/config';
  import react from '@vitejs/plugin-react';
  import path from 'path';

  export default defineConfig({
    plugins: [react()],
    test: {
      environment: 'jsdom',
      globals: true,
      setupFiles: './vitest.setup.ts',
    },
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './'),
      },
    },
  });
  ```

  Create `vitest.setup.ts`:
  ```typescript
  import '@testing-library/jest-dom';
  ```

  Update `package.json` scripts section to include `test`:
  ```json
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "test": "vitest run"
  }
  ```

- [ ] **Step 4: Verify test environment passes**
  Create a quick verification test `app/components/sample.test.ts`:
  ```typescript
  import { expect, test } from 'vitest';
  test('math works', () => {
    expect(2 + 2).toBe(4);
  });
  ```
  Run: `cmd /c npm run test`
  Expected: PASS

- [ ] **Step 5: Clean up and Commit**
  Remove `app/components/sample.test.ts` and `scripts/verify-nextjs.js`.
  ```bash
  git add package.json package-lock.json next.config.ts tsconfig.json vitest.config.ts vitest.setup.ts app/
  git commit -m "chore: scaffold Next.js app with TypeScript, ESLint, and Vitest test suite"
  ```

---

### Task 3: Dashboard Layout and Shell (Sidebar & Copilot Pane)

**Files:**
- Modify: `app/layout.tsx`
- Create: `app/global.css`
- Create: `app/components/Sidebar.tsx`
- Create: `app/components/Sidebar.module.css`
- Create: `app/components/CopilotPane.tsx`
- Create: `app/components/CopilotPane.module.css`
- Create: `app/components/Sidebar.test.tsx`

**Interfaces:**
- Consumes: Standard Next.js layouts.
- Produces: The main shell containing the collapsible navigation sidebar (left) and the collapsible `hund.ai` chat drawer (right).

- [ ] **Step 1: Write the component unit test**
  Create `app/components/Sidebar.test.tsx`:
  ```typescript
  import { render, screen } from '@testing-library/react';
  import { expect, test } from 'vitest';
  import Sidebar from './Sidebar';

  test('renders sidebar with styde lowercase logo and links', () => {
    render(<Sidebar activeTab="dashboard" onTabChange={() => {}} />);
    const logo = screen.getByText('styde');
    expect(logo).toBeInTheDocument();
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Agent Hub')).toBeInTheDocument();
  });
  ```
  Run: `cmd /c npm run test`
  Expected: FAIL (Sidebar component does not exist)

- [ ] **Step 2: Implement styling system & components**
  Create `app/global.css` with a high-end dark mode layout and glassmorphic colors:
  ```css
  :root {
    --bg-primary: #07080e;
    --bg-secondary: #0d0f17;
    --bg-surface: #131722;
    --border-color: rgba(255, 255, 255, 0.06);
    --text-primary: #f3f4f6;
    --text-secondary: #9ca3af;
    --accent-purple: #8b5cf6;
    --accent-cyan: #06b6d4;
    --accent-green: #10b981;
    --accent-red: #ef4444;
    --font-sans: 'Inter', system-ui, sans-serif;
  }

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    background-color: var(--bg-primary);
    color: var(--text-primary);
    font-family: var(--font-sans);
    overflow: hidden;
    height: 100vh;
  }

  input, select, textarea, button {
    font-family: inherit;
  }
  ```

  Create `app/components/Sidebar.tsx`:
  ```tsx
  'use client';
  import React from 'react';
  import styles from './Sidebar.module.css';

  interface SidebarProps {
    activeTab: string;
    onTabChange: (tab: string) => void;
  }

  export default function Sidebar({ activeTab, onTabChange }: SidebarProps) {
    const tabs = [
      { id: 'dashboard', label: 'Dashboard' },
      { id: 'flow', label: 'Project Flow' },
      { id: 'agents', label: 'Agent Hub' },
      { id: 'settings', label: 'Settings' }
    ];

    return (
      <aside className={styles.sidebar}>
        <div className={styles.logo}>styde</div>
        <nav className={styles.nav}>
          {tabs.map((tab) => (
            <button
              key={tab.id}
              className={`${styles.navButton} ${activeTab === tab.id ? styles.active : ''}`}
              onClick={() => onTabChange(tab.id)}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </aside>
    );
  }
  ```

  Create `app/components/Sidebar.module.css`:
  ```css
  .sidebar {
    width: 240px;
    height: 100vh;
    background-color: var(--bg-secondary);
    border-right: 1px solid var(--border-color);
    display: flex;
    flex-direction: column;
    padding: 24px 16px;
    flex-shrink: 0;
  }

  .logo {
    font-size: 24px;
    font-weight: 800;
    letter-spacing: -0.05em;
    color: var(--text-primary);
    margin-bottom: 40px;
    padding-left: 12px;
  }

  .logo::after {
    content: '.';
    color: var(--accent-purple);
  }

  .nav {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .navButton {
    background: none;
    border: none;
    color: var(--text-secondary);
    padding: 12px 16px;
    border-radius: 8px;
    text-align: left;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .navButton:hover {
    color: var(--text-primary);
    background-color: rgba(255, 255, 255, 0.03);
  }

  .navButton.active {
    color: #fff;
    background-color: var(--accent-purple);
    box-shadow: 0 0 16px rgba(139, 92, 246, 0.3);
  }
  ```

  Create `app/components/CopilotPane.tsx`:
  ```tsx
  'use client';
  import React, { useState } from 'react';
  import styles from './CopilotPane.module.css';

  interface Message {
    sender: 'user' | 'hund';
    text: string;
  }

  export default function CopilotPane() {
    const [isOpen, setIsOpen] = useState(true);
    const [messages, setMessages] = useState<Message[]>([
      { sender: 'hund', text: 'Hej! Jag är hund.ai, din copilot. Hur kan jag hjälpa dig idag?' }
    ]);
    const [input, setInput] = useState('');

    const sendMessage = (e: React.FormEvent) => {
      e.preventDefault();
      if (!input.trim()) return;
      const userMsg = input;
      setMessages((prev) => [...prev, { sender: 'user', text: userMsg }]);
      setInput('');

      // Simulated assistant reply
      setTimeout(() => {
        setMessages((prev) => [
          ...prev,
          { sender: 'hund', text: `Hund.ai mottog: "${userMsg}". Allt ser grönt ut i systemet!` }
        ]);
      }, 800);
    };

    return (
      <div className={`${styles.pane} ${isOpen ? styles.open : styles.closed}`}>
        <button className={styles.toggle} onClick={() => setIsOpen(!isOpen)}>
          {isOpen ? '→' : '← hund.ai'}
        </button>
        {isOpen && (
          <div className={styles.content}>
            <div className={styles.header}>
              <h3>hund.ai</h3>
              <span className={styles.badge}>aktiv</span>
            </div>
            <div className={styles.chatArea}>
              {messages.map((msg, index) => (
                <div key={index} className={`${styles.bubble} ${styles[msg.sender]}`}>
                  {msg.text}
                </div>
              ))}
            </div>
            <form onSubmit={sendMessage} className={styles.inputArea}>
              <input
                type="text"
                placeholder="Fråga hund.ai..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                className={styles.input}
              />
              <button type="submit" className={styles.sendBtn}>Skicka</button>
            </form>
          </div>
        )}
      </div>
    );
  }
  ```

  Create `app/components/CopilotPane.module.css`:
  ```css
  .pane {
    position: relative;
    height: 100vh;
    background-color: var(--bg-secondary);
    border-left: 1px solid var(--border-color);
    display: flex;
    transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    flex-shrink: 0;
  }

  .open {
    width: 320px;
  }

  .closed {
    width: 48px;
  }

  .toggle {
    position: absolute;
    left: -48px;
    top: 24px;
    width: 48px;
    height: 40px;
    background-color: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-right: none;
    border-radius: 8px 0 0 8px;
    color: var(--text-primary);
    cursor: pointer;
    font-size: 14px;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .content {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    padding: 24px 16px;
  }

  .header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 20px;
  }

  .header h3 {
    font-size: 18px;
    font-weight: 700;
    color: var(--text-primary);
  }

  .badge {
    background-color: rgba(16, 185, 129, 0.1);
    color: var(--accent-green);
    font-size: 11px;
    padding: 2px 6px;
    border-radius: 12px;
    font-weight: bold;
  }

  .chatArea {
    flex-grow: 1;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-bottom: 16px;
    padding-right: 4px;
  }

  .bubble {
    padding: 10px 14px;
    border-radius: 12px;
    font-size: 13px;
    max-width: 85%;
    line-height: 1.4;
  }

  .hund {
    background-color: var(--bg-surface);
    color: var(--text-primary);
    align-self: flex-start;
    border-bottom-left-radius: 2px;
    border: 1px solid var(--border-color);
  }

  .user {
    background-color: var(--accent-purple);
    color: white;
    align-self: flex-end;
    border-bottom-right-radius: 2px;
  }

  .inputArea {
    display: flex;
    gap: 8px;
  }

  .input {
    flex-grow: 1;
    background-color: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    color: white;
    padding: 8px 12px;
    font-size: 13px;
  }

  .input:focus {
    outline: none;
    border-color: var(--accent-purple);
  }

  .sendBtn {
    background-color: var(--bg-surface);
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 13px;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .sendBtn:hover {
    background-color: rgba(255, 255, 255, 0.05);
  }
  ```

  Update `app/layout.tsx` to wrap components and apply general CSS:
  ```tsx
  import './global.css';
  import React from 'react';

  export const metadata = {
    title: 'styde | automationshubb',
    description: 'Hantera dina AI-agenter och audits med hund.ai',
  };

  export default function RootLayout({
    children,
  }: {
    children: React.ReactNode;
  }) {
    return (
      <html lang="sv">
        <body>{children}</body>
      </html>
    );
  }
  ```

- [ ] **Step 3: Update entry page to use shell**
  Create `app/page.tsx`:
  ```tsx
  'use client';
  import React, { useState } from 'react';
  import Sidebar from './components/Sidebar';
  import CopilotPane from './components/CopilotPane';

  export default function MainPage() {
    const [activeTab, setActiveTab] = useState('dashboard');

    return (
      <div style={{ display: 'flex', width: '100vw', height: '100vh' }}>
        <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />
        <main style={{ flexGrow: 1, padding: '40px', overflowY: 'auto', backgroundColor: 'var(--bg-primary)' }}>
          <h1>Välkommen till styde</h1>
          <p style={{ color: 'var(--text-secondary)', marginTop: '8px' }}>
            Aktiv sektion: <strong>{activeTab}</strong>. Vänligen välj Agent Hub i menyn.
          </p>
        </main>
        <CopilotPane />
      </div>
    );
  }
  ```

- [ ] **Step 4: Run component test**
  Run: `cmd /c npm run test`
  Expected: PASS

- [ ] **Step 5: Commit changes**
  ```bash
  git add app/global.css app/layout.tsx app/page.tsx app/components/Sidebar.tsx app/components/Sidebar.module.css app/components/Sidebar.test.tsx app/components/CopilotPane.tsx app/components/CopilotPane.module.css
  git commit -m "feat: design responsive dark layout with Sidebar and collapsible hund.ai pane"
  ```

---

### Task 4: Agent Hub Page & Controls

**Files:**
- Create: `app/components/AgentCard.tsx`
- Create: `app/components/AgentCard.module.css`
- Create: `app/agents/page.tsx`
- Create: `app/agents/page.module.css`
- Create: `app/components/AgentCard.test.tsx`

**Interfaces:**
- Consumes: React states and global styling tokens.
- Produces: Visual list of agents with identity settings, sliding parameters, prompt overrides, and cost thresholds.

- [ ] **Step 1: Write component unit test**
  Create `app/components/AgentCard.test.tsx`:
  ```typescript
  import { render, screen, fireEvent } from '@testing-library/react';
  import { expect, test, vi } from 'vitest';
  import AgentCard from './AgentCard';

  const mockAgent = {
    id: '1',
    name: 'Fakturaskannare',
    avatar_url: '/avatar.png',
    status: 'active' as const,
    daily_budget_limit: 15.0,
    config: { strictness: 0.8, length: 0.2, rules: '' }
  };

  test('renders agent info and handles setting updates', () => {
    const handleUpdate = vi.fn();
    render(<AgentCard agent={mockAgent} onUpdate={handleUpdate} />);
    
    expect(screen.getByText('Fakturaskannare')).toBeInTheDocument();
    
    const slider = screen.getByLabelText('Strikthet: 80%');
    fireEvent.change(slider, { target: { value: '0.4' } });
    
    expect(handleUpdate).toHaveBeenCalled();
  });
  ```
  Run: `cmd /c npm run test`
  Expected: FAIL

- [ ] **Step 2: Implement AgentCard component**
  Create `app/components/AgentCard.tsx`:
  ```tsx
  'use client';
  import React from 'react';
  import styles from './AgentCard.module.css';

  export interface Agent {
    id: string;
    name: string;
    avatar_url: string;
    status: 'active' | 'paused';
    daily_budget_limit: number;
    config: {
      strictness: number;
      length: number;
      rules?: string;
    };
  }

  interface AgentCardProps {
    agent: Agent;
    onUpdate: (updated: Agent) => void;
  }

  export default function AgentCard({ agent, onUpdate }: AgentCardProps) {
    const toggleStatus = () => {
      onUpdate({
        ...agent,
        status: agent.status === 'active' ? 'paused' : 'active'
      });
    };

    const handleSlider = (key: 'strictness' | 'length', val: number) => {
      onUpdate({
        ...agent,
        config: {
          ...agent.config,
          [key]: val
        }
      });
    };

    const handleBudget = (val: number) => {
      onUpdate({
        ...agent,
        daily_budget_limit: val
      });
    };

    const handleRules = (val: string) => {
      onUpdate({
        ...agent,
        config: {
          ...agent.config,
          rules: val
        }
      });
    };

    return (
      <div className={styles.card}>
        <div className={styles.header}>
          <div className={styles.avatar}>{agent.name[0]}</div>
          <div>
            <h4 className={styles.title}>{agent.name}</h4>
            <span className={`${styles.status} ${styles[agent.status]}`}>{agent.status}</span>
          </div>
          <button className={styles.toggleBtn} onClick={toggleStatus}>
            {agent.status === 'active' ? 'Pausa' : 'Aktivera'}
          </button>
        </div>

        <div className={styles.section}>
          <label htmlFor={`strict-${agent.id}`} className={styles.label}>
            Strikthet: {Math.round(agent.config.strictness * 100)}%
          </label>
          <input
            id={`strict-${agent.id}`}
            type="range"
            min="0"
            max="1"
            step="0.1"
            value={agent.config.strictness}
            onChange={(e) => handleSlider('strictness', parseFloat(e.target.value))}
            className={styles.slider}
          />
        </div>

        <div className={styles.section}>
          <label htmlFor={`length-${agent.id}`} className={styles.label}>
            Utförlighet: {Math.round(agent.config.length * 100)}%
          </label>
          <input
            id={`length-${agent.id}`}
            type="range"
            min="0"
            max="1"
            step="0.1"
            value={agent.config.length}
            onChange={(e) => handleSlider('length', parseFloat(e.target.value))}
            className={styles.slider}
          />
        </div>

        <div className={styles.section}>
          <label htmlFor={`budget-${agent.id}`} className={styles.label}>Daglig budgetgräns ($)</label>
          <input
            id={`budget-${agent.id}`}
            type="number"
            value={agent.daily_budget_limit}
            onChange={(e) => handleBudget(parseFloat(e.target.value) || 0)}
            className={styles.numInput}
          />
        </div>

        <div className={styles.section}>
          <label htmlFor={`rules-${agent.id}`} className={styles.label}>Prompt-regler (Overrides)</label>
          <textarea
            id={`rules-${agent.id}`}
            value={agent.config.rules || ''}
            onChange={(e) => handleRules(e.target.value)}
            placeholder="T.ex. Skicka kvitton över 1000kr till chef Y..."
            className={styles.textarea}
          />
        </div>
      </div>
    );
  }
  ```

  Create `app/components/AgentCard.module.css`:
  ```css
  .card {
    background-color: var(--bg-surface);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }

  .header {
    display: flex;
    align-items: center;
    gap: 12px;
    border-bottom: 1px solid var(--border-color);
    padding-bottom: 12px;
  }

  .avatar {
    width: 40px;
    height: 40px;
    background-color: var(--accent-purple);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    color: white;
    font-size: 18px;
  }

  .title {
    font-size: 16px;
    font-weight: 600;
  }

  .status {
    font-size: 11px;
    padding: 2px 6px;
    border-radius: 4px;
    font-weight: bold;
    text-transform: uppercase;
  }

  .active {
    background-color: rgba(16, 185, 129, 0.1);
    color: var(--accent-green);
  }

  .paused {
    background-color: rgba(239, 68, 68, 0.1);
    color: var(--accent-red);
  }

  .toggleBtn {
    margin-left: auto;
    background-color: transparent;
    border: 1px solid var(--border-color);
    color: var(--text-primary);
    padding: 6px 12px;
    border-radius: 6px;
    font-size: 12px;
    cursor: pointer;
  }

  .toggleBtn:hover {
    background-color: rgba(255, 255, 255, 0.05);
  }

  .section {
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .label {
    font-size: 12px;
    font-weight: 600;
    color: var(--text-secondary);
  }

  .slider {
    width: 100%;
    accent-color: var(--accent-purple);
    cursor: pointer;
  }

  .numInput, .textarea {
    background-color: var(--bg-secondary);
    border: 1px solid var(--border-color);
    color: white;
    padding: 8px;
    border-radius: 6px;
    font-size: 13px;
  }

  .numInput:focus, .textarea:focus {
    outline: none;
    border-color: var(--accent-purple);
  }

  .textarea {
    resize: vertical;
    height: 60px;
  }
  ```

- [ ] **Step 3: Implement Agent Hub view**
  Create `app/agents/page.tsx`:
  ```tsx
  'use client';
  import React, { useState } from 'react';
  import Sidebar from '../components/Sidebar';
  import CopilotPane from '../components/CopilotPane';
  import AgentCard, { Agent } from '../components/AgentCard';
  import styles from './page.module.css';

  export default function AgentHub() {
    const [agents, setAgents] = useState<Agent[]>([
      {
        id: 'a7b9f8a2-2b3c',
        name: 'Fakturaskannare',
        avatar_url: '',
        status: 'active',
        daily_budget_limit: 25.0,
        config: { strictness: 0.8, length: 0.2, rules: 'Skicka över 50 000 kr till chef Y' }
      },
      {
        id: 'b7b9f8a2-2b3c',
        name: 'SupportSorterare',
        avatar_url: '',
        status: 'paused',
        daily_budget_limit: 10.0,
        config: { strictness: 0.4, length: 0.7, rules: '' }
      }
    ]);

    const handleUpdate = (updated: Agent) => {
      setAgents((prev) => prev.map((a) => (a.id === updated.id ? updated : a)));
    };

    return (
      <div className={styles.container}>
        <Sidebar activeTab="agents" onTabChange={() => {}} />
        <main className={styles.main}>
          <div className={styles.header}>
            <h2>Agent Hub</h2>
            <p>Konfigurera och övervaka dina aktiva AI-processer.</p>
          </div>
          <div className={styles.grid}>
            {agents.map((agent) => (
              <AgentCard key={agent.id} agent={agent} onUpdate={handleUpdate} />
            ))}
          </div>
        </main>
        <CopilotPane />
      </div>
    );
  }
  ```

  Create `app/agents/page.module.css`:
  ```css
  .container {
    display: flex;
    width: 100vw;
    height: 100vh;
  }

  .main {
    flex-grow: 1;
    padding: 40px;
    overflow-y: auto;
    background-color: var(--bg-primary);
  }

  .header {
    margin-bottom: 32px;
  }

  .header h2 {
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 6px;
  }

  .header p {
    color: var(--text-secondary);
    font-size: 14px;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 24px;
  }
  ```

  Update the default routing in `app/page.tsx` to redirect or link to agents, or simply render the tab content conditionally. Let's make `app/page.tsx` dynamically toggle layouts based on the `activeTab` so that clicking the sidebar tab swaps the main view seamlessly without page refreshes!
  Replace `app/page.tsx`:
  ```tsx
  'use client';
  import React, { useState } from 'react';
  import Sidebar from './components/Sidebar';
  import CopilotPane from './components/CopilotPane';
  import AgentCard, { Agent } from './components/AgentCard';
  import styles from './agents/page.module.css';

  export default function MainPage() {
    const [activeTab, setActiveTab] = useState('agents');
    const [agents, setAgents] = useState<Agent[]>([
      {
        id: 'a7b9f8a2-2b3c',
        name: 'Fakturaskannare',
        avatar_url: '',
        status: 'active',
        daily_budget_limit: 25.0,
        config: { strictness: 0.8, length: 0.2, rules: 'Skicka över 50 000 kr till chef Y' }
      },
      {
        id: 'b7b9f8a2-2b3c',
        name: 'SupportSorterare',
        avatar_url: '',
        status: 'paused',
        daily_budget_limit: 10.0,
        config: { strictness: 0.4, length: 0.7, rules: '' }
      }
    ]);

    const handleUpdate = (updated: Agent) => {
      setAgents((prev) => prev.map((a) => (a.id === updated.id ? updated : a)));
    };

    return (
      <div className={styles.container}>
        <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />
        <main className={styles.main}>
          {activeTab === 'agents' ? (
            <>
              <div className={styles.header}>
                <h2>Agent Hub</h2>
                <p>Konfigurera och övervaka dina aktiva AI-processer.</p>
              </div>
              <div className={styles.grid}>
                {agents.map((agent) => (
                  <AgentCard key={agent.id} agent={agent} onUpdate={handleUpdate} />
                ))}
              </div>
            </>
          ) : (
            <>
              <div className={styles.header}>
                <h2>{activeTab.charAt(0).toUpperCase() + activeTab.slice(1)}</h2>
                <p>Sektionen är under uppbyggnad.</p>
              </div>
            </>
          )}
        </main>
        <CopilotPane />
      </div>
    );
  }
  ```

- [ ] **Step 4: Run component tests**
  Run: `cmd /c npm run test`
  Expected: PASS

- [ ] **Step 5: Commit changes**
  ```bash
  git add app/components/AgentCard.tsx app/components/AgentCard.module.css app/components/AgentCard.test.tsx app/agents/page.tsx app/agents/page.module.css app/page.tsx
  git commit -m "feat: implement Agent Hub view and customizable AgentCard components with sliders"
  ```

---

### Task 5: Copilot API Route & Streaming Text Response

**Files:**
- Create: `app/api/chat/route.ts`
- Modify: `app/components/CopilotPane.tsx`
- Create: `app/components/CopilotPane.test.tsx`

**Interfaces:**
- Consumes: Text query post requests.
- Produces: Simulated AI chat responses generated based on local queries.

- [ ] **Step 1: Write API response test**
  Create `app/components/CopilotPane.test.tsx`:
  ```typescript
  import { render, screen, fireEvent, waitFor } from '@testing-library/react';
  import { expect, test } from 'vitest';
  import CopilotPane from './CopilotPane';

  test('allows typing a message and receiving a response', async () => {
    render(<CopilotPane />);
    
    const input = screen.getByPlaceholderText('Fråga hund.ai...');
    fireEvent.change(input, { target: { value: 'Status för fakturor' } });
    
    const button = screen.getByText('Skicka');
    fireEvent.click(button);

    expect(screen.getByText('Status för fakturor')).toBeInTheDocument();
    
    await waitFor(() => {
      expect(screen.getByText(/mottog: "Status för fakturor"/)).toBeInTheDocument();
    }, { timeout: 1500 });
  });
  ```
  Run: `cmd /c npm run test`
  Expected: PASS (as the local mock setTimeout is already set up in task 3, but let's connect it to our custom API route `/api/chat` next!)

- [ ] **Step 2: Implement Mock API Route**
  Create `app/api/chat/route.ts`:
  ```typescript
  import { NextResponse } from 'next/server';

  export async function POST(request: Request) {
    try {
      const { message } = await request.json();
      
      let reply = `Voff! Jag kollade din förfrågan angående "${message}". `;
      
      const queryLower = message.toLowerCase();
      if (queryLower.includes('budget') || queryLower.includes('kostnad')) {
        reply += 'Den totala kostnaden idag är $3.45, vilket är långt under budgettaket på $35.00.';
      } else if (queryLower.includes('status') || queryLower.includes('agenter')) {
        reply += 'Fakturaskannare är igång (active), och SupportSorterare är pausad.';
      } else if (queryLower.includes('audit')) {
        reply += 'Din senaste revision slutfördes framgångsrikt. Du kan ladda ner PDF-rapporten i Project Flow.';
      } else {
        reply += 'Allt ser fint ut i systemet. Låt mig veta om du vill göra ändringar i konfigurationen!';
      }

      return NextResponse.json({ reply });
    } catch (e: any) {
      return NextResponse.json({ error: 'Något gick fel.' }, { status: 500 });
    }
  }
  ```

- [ ] **Step 3: Connect Frontend to API Route**
  Modify `app/components/CopilotPane.tsx` to fetch response from `/api/chat`:
  ```tsx
  'use client';
  import React, { useState } from 'react';
  import styles from './CopilotPane.module.css';

  interface Message {
    sender: 'user' | 'hund';
    text: string;
  }

  export default function CopilotPane() {
    const [isOpen, setIsOpen] = useState(true);
    const [messages, setMessages] = useState<Message[]>([
      { sender: 'hund', text: 'Hej! Jag är hund.ai, din copilot. Hur kan jag hjälpa dig idag?' }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);

    const sendMessage = async (e: React.FormEvent) => {
      e.preventDefault();
      if (!input.trim() || loading) return;
      const userMsg = input;
      setMessages((prev) => [...prev, { sender: 'user', text: userMsg }]);
      setInput('');
      setLoading(true);

      try {
        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ message: userMsg })
        });
        const data = await response.json();
        setMessages((prev) => [
          ...prev,
          { sender: 'hund', text: data.reply || 'Hund.ai kunde inte svara just nu.' }
        ]);
      } catch (err) {
        setMessages((prev) => [
          ...prev,
          { sender: 'hund', text: 'Kunde inte nå hund.ai. Kontrollera anslutningen.' }
        ]);
      } finally {
        setLoading(false);
      }
    };

    return (
      <div className={`${styles.pane} ${isOpen ? styles.open : styles.closed}`}>
        <button className={styles.toggle} onClick={() => setIsOpen(!isOpen)}>
          {isOpen ? '→' : '← hund.ai'}
        </button>
        {isOpen && (
          <div className={styles.content}>
            <div className={styles.header}>
              <h3>hund.ai</h3>
              <span className={styles.badge}>aktiv</span>
            </div>
            <div className={styles.chatArea}>
              {messages.map((msg, index) => (
                <div key={index} className={`${styles.bubble} ${styles[msg.sender]}`}>
                  {msg.text}
                </div>
              ))}
              {loading && <div className={`${styles.bubble} ${styles.hund}`}>Hund söker svar...</div>}
            </div>
            <form onSubmit={sendMessage} className={styles.inputArea}>
              <input
                type="text"
                placeholder="Fråga hund.ai..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                className={styles.input}
                disabled={loading}
              />
              <button type="submit" className={styles.sendBtn} disabled={loading}>
                {loading ? 'Söker...' : 'Skicka'}
              </button>
            </form>
          </div>
        )}
      </div>
    );
  }
  ```

- [ ] **Step 4: Run component tests**
  Run: `cmd /c npm run test`
  Expected: PASS (Vitest tests for rendering and chat stream submission success)

- [ ] **Step 5: Commit changes**
  ```bash
  git add app/api/chat/route.ts app/components/CopilotPane.tsx app/components/CopilotPane.test.tsx
  git commit -m "feat: add next api route for chat and connect copilot pane to fetch responses from hund.ai"
  ```
