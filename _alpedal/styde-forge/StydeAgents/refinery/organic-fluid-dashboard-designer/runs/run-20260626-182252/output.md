<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>dwell — organic dashboard</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI','Inter',system-ui,-apple-system,sans-serif;background:#faf5f0;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px;color:#2c2418}
.dashboard{max-width:1100px;width:100%;background:linear-gradient(145deg,#fff8f0,#f0ebe0);border-radius:48px;padding:40px;box-shadow:0 20px 60px rgba(100,70,40,0.10),0 8px 24px rgba(100,70,40,0.06),inset 0 1px 0 rgba(255,255,245,0.6)}
.header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:40px;flex-wrap:wrap;gap:16px}
.header-left{display:flex;flex-direction:column;gap:4px}
.greeting{font-size:14px;color:#8a7a68;letter-spacing:0.3px;font-weight:400}
.greeting span{color:#b8a088}
h1{font-size:28px;font-weight:500;color:#2c2418;line-height:1.2;letter-spacing:-0.3px}
h1 small{font-weight:300;color:#8a7a68;display:block;font-size:16px;margin-top:2px}
.header-actions{display:flex;gap:12px;align-items:center}
.icon-btn{width:44px;height:44px;border-radius:50%;border:none;background:linear-gradient(135deg,#fff,#f5efe8);box-shadow:0 2px 8px rgba(100,70,40,0.06);cursor:pointer;font-size:18px;display:flex;align-items:center;justify-content:center;transition:all 0.25s ease;color:#6b5d4e;position:relative}
.icon-btn:hover{transform:scale(1.08);box-shadow:0 4px 16px rgba(160,120,80,0.15);background:linear-gradient(135deg,#fff,#ede4d8)}
.icon-btn:focus-visible{outline:3px solid #c4a882;outline-offset:3px;border-radius:50%}
.icon-btn .badge{position:absolute;top:-2px;right:-2px;width:18px;height:18px;border-radius:50%;background:#d68b7a;color:#fff;font-size:10px;font-weight:600;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 6px rgba(214,139,122,0.3)}
.avatar{width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,#dbb88c,#c49a6e);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:500;font-size:16px;cursor:pointer;transition:transform 0.25s ease,box-shadow 0.25s ease;box-shadow:0 2px 8px rgba(160,120,80,0.12);border:2px solid rgba(255,255,245,0.5)}
.avatar:hover{transform:scale(1.06);box-shadow:0 4px 16px rgba(160,120,80,0.2)}
.avatar:focus-visible{outline:3px solid #c4a882;outline-offset:3px}
.welcome-card{background:linear-gradient(135deg,#f5ede2,#ede0d0);border-radius:32px;padding:32px;margin-bottom:32px;display:flex;align-items:center;gap:24px;flex-wrap:wrap;box-shadow:inset 0 1px 0 rgba(255,255,245,0.6)}
.welcome-text{flex:1;min-width:200px}
.welcome-text h2{font-size:22px;font-weight:500;color:#2c2418;margin-bottom:8px}
.welcome-text p{font-size:14px;color:#7a6a58;line-height:1.5;margin-bottom:16px}
.welcome-text .pill-group{display:flex;gap:8px;flex-wrap:wrap}
.pill{display:inline-flex;align-items:center;gap:6px;padding:8px 16px;border-radius:50px;background:rgba(255,255,245,0.55);border:1px solid rgba(200,180,160,0.2);font-size:13px;color:#5a4a38;cursor:pointer;transition:all 0.2s ease}
.pill:hover{background:rgba(255,255,245,0.85);border-color:#c4a882;transform:translateY(-1px)}
.pill.active{background:#c4a882;color:#fff;border-color:#c4a882}
.pill:focus-visible{outline:3px solid #c4a882;outline-offset:2px}
.welcome-visual{width:100px;height:100px;border-radius:50%;background:radial-gradient(circle at 30% 30%,#e8d5b8,#c9af8b);display:flex;align-items:center;justify-content:center;font-size:42px;box-shadow:0 8px 24px rgba(160,120,80,0.12)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px;margin-bottom:32px}
.card{background:rgba(255,255,245,0.45);backdrop-filter:blur(4px);border-radius:28px;padding:24px;border:1px solid rgba(255,255,245,0.8);transition:all 0.3s ease;cursor:pointer;position:relative;overflow:hidden}
.card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,transparent,var(--accent,#c4a882),transparent);opacity:0;transition:opacity 0.3s ease}
.card:hover{transform:translateY(-4px);box-shadow:0 12px 32px rgba(100,70,40,0.08);border-color:rgba(200,180,160,0.3)}
.card:hover::before{opacity:1}
.card:focus-visible{outline:3px solid #c4a882;outline-offset:3px}
.card-icon{width:40px;height:40px;border-radius:16px;background:linear-gradient(135deg,var(--icon-bg1,#f0e4d4),var(--icon-bg2,#e4d4c0));display:flex;align-items:center;justify-content:center;font-size:18px;margin-bottom:14px}
.card h3{font-size:16px;font-weight:500;color:#2c2418;margin-bottom:4px}
.card .value{font-size:28px;font-weight:500;color:#3c3024;margin-bottom:2px;letter-spacing:-0.5px}
.card .trend{font-size:13px;display:flex;align-items:center;gap:4px}
.card .trend.up{color:#7a9a6a}
.card .trend.down{color:#c47a6a}
.card .trend.neutral{color:#8a7a68}
.card .sub{font-size:12px;color:#9a8a78;margin-top:2px}
.bottom-row{display:grid;grid-template-columns:2fr 1fr;gap:20px}@media(max-width:640px){.bottom-row{grid-template-columns:1fr}}
.activity-section{background:rgba(255,255,245,0.45);backdrop-filter:blur(4px);border-radius:28px;padding:24px;border:1px solid rgba(255,255,245,0.8)}
.activity-section h3{font-size:16px;font-weight:500;color:#2c2418;margin-bottom:16px}
.activity-item{display:flex;align-items:flex-start;gap:14px;padding:12px 0;border-bottom:1px solid rgba(200,180,160,0.12);transition:background 0.2s ease;border-radius:12px;cursor:pointer;padding:12px}
.activity-item:last-child{border-bottom:none}
.activity-item:hover{background:rgba(200,180,160,0.06)}
.activity-item:focus-visible{outline:2px solid #c4a882;outline-offset:2px}
.activity-dot{width:10px;height:10px;border-radius:50%;margin-top:5px;flex-shrink:0}
.activity-dot.green{background:#8db87a}
.activity-dot.amber{background:#d4a86a}
.activity-dot.blue{background:#7aabd8}
.activity-content{flex:1}
.activity-content p{font-size:13px;color:#3c3024;line-height:1.4}
.activity-content .time{font-size:11px;color:#9a8a78;margin-top:2px}
.quick-actions{display:flex;flex-direction:column;gap:10px}
.quick-action{display:flex;align-items:center;gap:14px;padding:16px 20px;border-radius:20px;background:rgba(255,255,245,0.45);backdrop-filter:blur(4px);border:1px solid rgba(255,255,245,0.8);cursor:pointer;transition:all 0.25s ease;font-size:14px;color:#3c3024}
.quick-action:hover{transform:translateX(4px);box-shadow:0 4px 16px rgba(100,70,40,0.06);border-color:#c4a882;background:rgba(255,255,245,0.7)}
.quick-action:focus-visible{outline:3px solid #c4a882;outline-offset:2px}
.quick-action .qa-icon{width:36px;height:36px;border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:16px}
.qa-create{background:linear-gradient(135deg,#e8dcc8,#d8c8b0)}
.qa-upload{background:linear-gradient(135deg,#d8e4c8,#c4d4b0)}
.qa-share{background:linear-gradient(135deg,#d8c8d8,#c4b4c4)}
.qa-settings{background:linear-gradient(135deg,#d8d4e0,#c4c0d0)}
.footer{display:flex;justify-content:space-between;align-items:center;margin-top:32px;padding-top:20px;border-top:1px solid rgba(200,180,160,0.15);flex-wrap:wrap;gap:12px}
.footer p{font-size:12px;color:#9a8a78}
.footer-links{display:flex;gap:16px}
.footer-links a{font-size:12px;color:#8a7a68;text-decoration:none;transition:color 0.2s ease;cursor:pointer}
.footer-links a:hover{color:#5a4a38}
.footer-links a:focus-visible{outline:2px solid #c4a882;outline-offset:2px}
input[type="search"]{border:none;background:rgba(255,255,245,0.5);border-radius:50px;padding:10px 18px;font-size:14px;color:#2c2418;width:200px;transition:all 0.25s ease;border:1px solid transparent}
input[type="search"]:focus{outline:none;border-color:#c4a882;background:rgba(255,255,245,0.8);width:240px;box-shadow:0 2px 8px rgba(160,120,80,0.06)}
input[type="search"]::placeholder{color:#b0a090}
input[type="search"]:focus-visible{outline:3px solid #c4a882;outline-offset:2px}
</style>
</head>
<body>
<div class="dashboard" role="main" aria-label="Organic dashboard">
<div class="header">
<div class="header-left">
<p class="greeting" aria-label="Current time greeting">good afternoon <span>·</span> 23°C partly sunny</p>
<h1>welcome back, elara <small>your studio is humming along</small></h1>
</div>
<div class="header-actions">
<input type="search" placeholder="search anything..." aria-label="Search your dashboard">
<button class="icon-btn" aria-label="View notifications"><span aria-hidden="true">&#9830;</span><span class="badge" aria-label="3 unread notifications">3</span></button>
<button class="icon-btn" aria-label="Open quick menu"><span aria-hidden="true">&#8226;&#8226;&#8226;</span></button>
<div class="avatar" tabindex="0" role="button" aria-label="Open user profile">EA</div>
</div>
</div>
<div class="welcome-card" role="region" aria-label="Daily overview">
<div class="welcome-text">
<h2>your day in motion</h2>
<p>3 projects have updates, 2 need your review. gentle nudges, nothing urgent.</p>
<div class="pill-group" role="group" aria-label="Quick filters">
<span class="pill active" tabindex="0" role="button" aria-pressed="true">projects</span>
<span class="pill" tabindex="0" role="button" aria-pressed="false">shared with me</span>
<span class="pill" tabindex="0" role="button" aria-pressed="false">drafts</span>
<span class="pill" tabindex="0" role="button" aria-pressed="false">archived</span>
</div>
</div>
<div class="welcome-visual" aria-hidden="true" role="img" aria-label="Decorative organic shape">&#9675;</div>
</div>
<div class="grid" role="region" aria-label="Key metrics">
<div class="card" tabindex="0" role="button" aria-label="Active projects metric: 12 active" style="--accent:#8db87a;--icon-bg1:#e0ecce;--icon-bg2:#c8dcb0">
<div class="card-icon" aria-hidden="true">&#9679;</div>
<h3>active projects</h3>
<div class="value">12</div>
<div class="trend up"><span aria-hidden="true">&#8593;</span> +2 this week</div>
<div class="sub">4 nearing completion</div>
</div>
<div class="card" tabindex="0" role="button" aria-label="Pending reviews metric: 5 items" style="--accent:#d4a86a;--icon-bg1:#f0e0c8;--icon-bg2:#e4d0b0">
<div class="card-icon" aria-hidden="true">&#9671;</div>
<h3>pending reviews</h3>
<div class="value">5</div>
<div class="trend up"><span aria-hidden="true">&#8593;</span> +1 since yesterday</div>
<div class="sub">2 high priority</div>
</div>
<div class="card" tabindex="0" role="button" aria-label="Team members metric: 8 online" style="--accent:#7aabd8;--icon-bg1:#c8d8e8;--icon-bg2:#b0c8dc">
<div class="card-icon" aria-hidden="true">&#9673;</div>
<h3>team members</h3>
<div class="value">8</div>
<div class="trend neutral"><span aria-hidden="true">&#8596;</span> 12 total on team</div>
<div class="sub">3 away</div>
</div>
<div class="card" tabindex="0" role="button" aria-label="Storage used metric: 68 percent" style="--accent:#c4a882;--icon-bg1:#f0e4d4;--icon-bg2:#e4d4c0">
<div class="card-icon" aria-hidden="true">&#9675;</div>
<h3>storage used</h3>
<div class="value">68%</div>
<div class="trend down"><span aria-hidden="true">&#8595;</span> -4% after cleanup</div>
<div class="sub">24.2 GB of 35 GB</div>
</div>
</div>
<div class="bottom-row">
<div class="activity-section" role="region" aria-label="Recent activity">
<h3>recent activity</h3>
<div class="activity-item" tabindex="0" role="button" aria-label="Activity: Elara commented on Flow State">
<div class="activity-dot green" aria-hidden="true"></div>
<div class="activity-content">
<p>Elara commented on <strong>Flow State</strong></p>
<div class="time">12 minutes ago</div>
</div>
</div>
<div class="activity-item" tabindex="0" role="button" aria-label="Activity: Studio renamed to Warm Hearth">
<div class="activity-dot amber" aria-hidden="true"></div>
<div class="activity-content">
<p>Studio renamed to <strong>Warm Hearth</strong></p>
<div class="time">1 hour ago</div>
</div>
</div>
<div class="activity-item" tabindex="0" role="button" aria-label="Activity: Jonas uploaded reference images">
<div class="activity-dot blue" aria-hidden="true"></div>
<div class="activity-content">
<p>Jonas uploaded <strong>4 reference images</strong></p>
<div class="time">3 hours ago</div>
</div>
</div>
<div class="activity-item" tabindex="0" role="button" aria-label="Activity: Weekly sync notes are ready">
<div class="activity-dot green" aria-hidden="true"></div>
<div class="activity-content">
<p>Weekly sync notes are <strong>ready</strong></p>
<div class="time">5 hours ago</div>
</div>
</div>
</div>
<div role="region" aria-label="Quick actions">
<div class="quick-actions">
<div class="quick-action" tabindex="0" role="button" aria-label="Create new project">
<div class="qa-icon qa-create" aria-hidden="true">+</div>
create project
</div>
<div class="quick-action" tabindex="0" role="button" aria-label="Upload files">
<div class="qa-icon qa-upload" aria-hidden="true">&#8593;</div>
upload files
</div>
<div class="quick-action" tabindex="0" role="button" aria-label="Share current dashboard">
<div class="qa-icon qa-share" aria-hidden="true">&#8594;</div>
share dashboard
</div>
<div class="quick-action" tabindex="0" role="button" aria-label="Open settings">
<div class="qa-icon qa-settings" aria-hidden="true">&#9881;</div>
settings
</div>
</div>
</div>
</div>
<div class="footer">
<p>dwell &mdash; an organic workspace</p>
<div class="footer-links">
<a tabindex="0" role="link">privacy</a>
<a tabindex="0" role="link">terms</a>
<a tabindex="0" role="link">feedback</a>
<a tabindex="0" role="link">shortcuts</a>
</div>
</div>
</div>
</body>
</html>