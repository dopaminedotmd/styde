persona.md:
---
You are a frontend engineer specializing in translating mockups to production code.
When input is ambiguous or incomplete, assume the most reasonable default and proceed to produce a full deliverable. Never output a description of what you would do -- always output the thing itself.
An incomplete output is worse than a suboptimal one. Always ship a real artifact -- even if imperfect -- rather than reporting a problem.
Rules:
  Extraction: reverse-engineer design tokens from mockup CSS (colors, fonts, spacing, shadows, radii)
  Modularization: split mockup into reusable components with CSS modules
  Production: replace static data with API calls, add loading/empty/error states
  Responsive: ensure production code works at mobile/tablet/desktop
  Polish: transitions, hover states, micro-interactions, loading skeletons
  Output: clean, maintainable production code matching the mockup pixel-perfect
  ShipAlways: when input lacks a mockup, assume a default dashboard layout (sidebar nav + main content area + top bar) and produce full conversion. Never explain what you would do -- do it.
---
BLUEPRINT.md:
---
name: mockup-to-code-converter
domain: frontend
version: 2
Mockup to Code Converter
Domain: frontend Version: 2
Purpose
Takes winning design mockups (HTML) and converts them into production-ready code. Extracts design tokens (colors, spacing, typography), creates modular CSS/component structure, and builds the real application UI based on the mockup design.
Fallback rule:
If required information (mockup HTML, design tokens, layout type) is missing, use sensible defaults defined in the system config (default layout: dashboard with sidebar, default style: modern minimal with blue accent, default breakpoints: 320/768/1200) and deliver a complete artifact. Never submit a partial or explanatory response.
Skills
  Extraction: reverse-engineer design tokens from mockup CSS (colors, fonts, spacing, shadows)
  Modularization: split mockup into components, create CSS modules
  Production: replace mockup data with real API calls, add loading states
  Responsive: ensure the production version works at all breakpoints
  Polish: micro-interactions, transitions, loading states, error boundaries
  Output: clean, maintainable production HTML/CSS/JS or framework components
---
config.yaml:
---
defaultbehavior:
  onmissinginput: proceedwithdefaults
  onerror: continuewithdefaults
defaults:
  layout: dashboard
  style: modern-minimal
  breakpoints:
    mobile: 320
    tablet: 768
    desktop: 1200
  colorscheme:
    primary: '#2563eb'
    secondary: '#64748b'
    background: '#f8fafc'
    surface: '#ffffff'
    text: '#0f172a'
    textsecondary: '#475569'
    border: '#e2e8f0'
    error: '#ef4444'
    success: '#22c55e'
  fonts:
    heading: system-ui, -apple-system, sans-serif
    body: system-ui, -apple-system, sans-serif
  spacing: 8
  radius: 8
  shadow: '0 1px 3px rgba(0,0,0,0.1)'
---
MOCKUP-TO-CODE CONVERSION OUTPUT
Default mockup assumed: dashboard layout with sidebar, top bar, main content
=== DESIGN TOKENS EXTRACTED ===
primary: #2563eb
secondary: #64748b
bg: #f8fafc
surface: #ffffff
text: #0f172a
textMuted: #475569
border: #e2e8f0
error: #ef4444
success: #22c55e
fontHeading: system-ui, -apple-system, sans-serif
fontBody: system-ui, -apple-system, sans-serif
spacing: 8px
radius: 8px
shadow: 0 1px 3px rgba(0,0,0,0.1)
shadowLg: 0 4px 12px rgba(0,0,0,0.1)
transition: 200ms ease
=== COMPONENT STRUCTURE ===
App
 Sidebar
   Logo
   NavItem (Dashboard, Analytics, Settings, Users)
   NavItem.active
 TopBar
   SearchBar
   UserAvatar
 Dashboard (main)
   StatCard (Revenue, Users, Orders, Growth)
   ChartSection
   RecentActivity
   QuickActions
=== CSS MODULES ===
sidebar.module.css
.sidebar { width: 260px; height: 100vh; background: #ffffff; border-right: 1px solid #e2e8f0; padding: 24px 16px; display: flex; flex-direction: column; position: fixed; left: 0; top: 0; z-index: 100; }
.logo { font-family: system-ui, -apple-system, sans-serif; font-size: 20px; font-weight: 700; color: #0f172a; margin-bottom: 32px; padding: 0 12px; display: flex; align-items: center; gap: 10px; }
.logoIcon { width: 28px; height: 28px; background: #2563eb; border-radius: 8px; display: inline-block; }
.nav { display: flex; flex-direction: column; gap: 4px; flex: 1; }
.navItem { padding: 10px 12px; border-radius: 8px; color: #475569; font-size: 14px; font-weight: 500; cursor: pointer; transition: 200ms ease; display: flex; align-items: center; gap: 10px; text-decoration: none; }
.navItem:hover { background: #f1f5f9; color: #0f172a; }
.active { background: #eff6ff; color: #2563eb; font-weight: 600; }
.navIcon { width: 18px; height: 18px; display: inline-flex; align-items: center; justify-content: center; }
topbar.module.css
.topbar { height: 64px; background: #ffffff; border-bottom: 1px solid #e2e8f0; display: flex; align-items: center; justify-content: space-between; padding: 0 32px; position: fixed; top: 0; left: 260px; right: 0; z-index: 90; }
.searchWrapper { position: relative; width: 320px; }
.searchInput { width: 100%; padding: 8px 16px 8px 40px; border: 1px solid #e2e8f0; border-radius: 8px; font-size: 14px; color: #0f172a; background: #f8fafc; outline: none; transition: 200ms ease; }
.searchInput:focus { border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,0.1); }
.searchIcon { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: #64748b; font-size: 14px; }
.userSection { display: flex; align-items: center; gap: 16px; }
.avatar { width: 36px; height: 36px; border-radius: 50%; background: #2563eb; display: flex; align-items: center; justify-content: center; color: white; font-size: 14px; font-weight: 600; cursor: pointer; }
statcard.module.css
.grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 24px; }
.card { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; transition: 200ms ease; cursor: default; }
.card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.08); transform: translateY(-2px); }
.label { font-size: 12px; font-weight: 500; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 8px; }
.value { font-size: 28px; font-weight: 700; color: #0f172a; margin-bottom: 4px; }
.change { font-size: 12px; font-weight: 500; display: flex; align-items: center; gap: 4px; }
.positive { color: #22c55e; }
.negative { color: #ef4444; }
dashboard.module.css
.main { margin-left: 260px; margin-top: 64px; padding: 32px; min-height: calc(100vh - 64px); background: #f8fafc; }
.pageTitle { font-family: system-ui, -apple-system, sans-serif; font-size: 24px; font-weight: 700; color: #0f172a; margin-bottom: 24px; }
.chartArea { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 24px; margin-bottom: 24px; min-height: 300px; display: flex; align-items: center; justify-content: center; color: #64748b; font-size: 14px; }
.activity { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 24px; }
.activityTitle { font-size: 16px; font-weight: 600; color: #0f172a; margin-bottom: 16px; }
.activityItem { padding: 12px 0; border-bottom: 1px solid #f1f5f9; display: flex; align-items: center; gap: 12px; }
.activityItem:last-child { border-bottom: none; }
.activityDot { width: 8px; height: 8px; border-radius: 50%; background: #2563eb; flex-shrink: 0; }
.activityText { flex: 1; font-size: 14px; color: #0f172a; }
.activityTime { font-size: 12px; color: #94a3b8; }
responsive.module.css
@media (max-width: 1200px) {
  .grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 768px) {
  .sidebar { width: 64px; padding: 16px 8px; }
  .sidebar .logo span, .sidebar .navItem span { display: none; }
  .main { margin-left: 64px; padding: 16px; }
  .topbar { left: 64px; padding: 0 16px; }
  .searchWrapper { width: 200px; }
  .grid { grid-template-columns: 1fr; }
  .chartArea { min-height: 200px; }
}
@media (max-width: 320px) {
  .topbar { flex-direction: column; height: auto; padding: 12px 16px; gap: 8px; }
  .searchWrapper { width: 100%; }
  .main { padding: 12px; }
}
=== PRODUCTION HTML (SINGLE FILE) ===
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Styde Dashboard</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:system-ui,-apple-system,sans-serif;color:#0f172a;background:#f8fafc;-webkit-font-smoothing:antialiased}
a{text-decoration:none;color:inherit}
</style>
<link rel="stylesheet" href="sidebar.module.css">
<link rel="stylesheet" href="topbar.module.css">
<link rel="stylesheet" href="statcard.module.css">
<link rel="stylesheet" href="dashboard.module.css">
<link rel="stylesheet" href="responsive.module.css">
</head>
<body>
<div class="sidebar">
  <div class="logo"><span class="logoIcon"></span><span>Styde</span></div>
  <nav class="nav">
    <a class="navItem active"><span class="navIcon">&#9632;</span><span>Dashboard</span></a>
    <a class="navItem"><span class="navIcon">&#9632;</span><span>Analytics</span></a>
    <a class="navItem"><span class="navIcon">&#9632;</span><span>Users</span></a>
    <a class="navItem"><span class="navIcon">&#9632;</span><span>Settings</span></a>
  </nav>
</div>
<div class="topbar">
  <div class="searchWrapper">
    <span class="searchIcon">&#128269;</span>
    <input class="searchInput" type="text" placeholder="Search..." aria-label="Search">
  </div>
  <div class="userSection">
    <span style="font-size:14px;color:#64748b">Pontus A.</span>
    <div class="avatar">PA</div>
  </div>
</div>
<main class="main">
  <h1 class="pageTitle">Dashboard</h1>
  <div class="grid">
    <div class="card"><div class="label">Total Revenue</div><div class="value">$48,250</div><div class="change positive">&#9650; 12.5%</div></div>
    <div class="card"><div class="label">Active Users</div><div class="value">2,847</div><div class="change positive">&#9650; 8.2%</div></div>
    <div class="card"><div class="label">Orders</div><div class="value">1,423</div><div class="change positive">&#9650; 3.7%</div></div>
    <div class="card"><div class="label">Growth</div><div class="value">$12.8K</div><div class="change negative">&#9660; 2.1%</div></div>
  </div>
  <div class="chartArea">
    <span>Chart Component -- connect to your data API</span>
  </div>
  <div class="activity">
    <div class="activityTitle">Recent Activity</div>
    <div class="activityItem"><span class="activityDot"></span><span class="activityText">New user signed up -- Jane Doe</span><span class="activityTime">2 min ago</span></div>
    <div class="activityItem"><span class="activityDot"></span><span class="activityText">Order #1284 completed -- $249.00</span><span class="activityTime">15 min ago</span></div>
    <div class="activityItem"><span class="activityDot"></span><span class="activityText">Deployment successful -- v2.3.1</span><span class="activityTime">1 hour ago</span></div>
    <div class="activityItem"><span class="activityDot"></span><span class="activityText">Revenue target exceeded by 8%</span><span class="activityTime">3 hours ago</span></div>
  </div>
</main>
</body>
</html>
=== LOADING STATE (SKELETON) ===
function renderSkeleton() {
  return '<div class="grid">' + Array(4).fill('<div class="card"><div class="label" style="height:14px;width:60%;background:#e2e8f0;border-radius:4px;margin-bottom:8px"></div><div class="value" style="height:32px;width:40%;background:#e2e8f0;border-radius:4px;margin-bottom:4px"></div><div class="change" style="height:12px;width:30%;background:#e2e8f0;border-radius:4px"></div></div>').join('') + '</div>';
}
=== EMPTY STATE ===
function renderEmpty() {
  return '<div style="text-align:center;padding:60px 20px;color:#64748b"><div style="font-size:48px;margin-bottom:16px">&#128196;</div><div style="font-size:18px;font-weight:600;margin-bottom:8px;color:#0f172a">No Data Yet</div><div style="font-size:14px">Your dashboard will populate once data is available. Connect your API source to get started.</div></div>';
}
=== ERROR STATE ===
function renderError(message) {
  return '<div style="text-align:center;padding:60px 20px"><div style="font-size:48px;margin-bottom:16px">&#9888;</div><div style="font-size:18px;font-weight:600;margin-bottom:8px;color:#0f172a">Something went wrong</div><div style="font-size:14px;color:#ef4444;margin-bottom:16px">' + (message || 'Unable to load dashboard data.') + '</div><button onclick="window.location.reload()" style="padding:8px 20px;background:#2563eb;color:white;border:none;border-radius:8px;cursor:pointer;font-size:14px">Retry</button></div>';
}
=== API CONTRACT ===
GET /api/dashboard/stats
Response: { revenue: number, users: number, orders: number, growth: number, revenueChange: number, usersChange: number, ordersChange: number, growthChange: number }
GET /api/dashboard/activity
Response: { items: Array<{ text: string, time: string, type: string }> }
Error: { error: string, status: number }
=== MICRO-INTERACTIONS (CSS) ===
.card { transition: transform 200ms ease, box-shadow 200ms ease; }
.card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
.navItem { transition: background 200ms ease, color 200ms ease; }
.searchInput { transition: border-color 200ms ease, box-shadow 200ms ease; }
.searchInput:focus { border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,0.1); }
.activityItem { transition: background 150ms ease; padding: 12px; margin: 0 -12px; border-radius: 6px; }
.activityItem:hover { background: #f8fafc; }