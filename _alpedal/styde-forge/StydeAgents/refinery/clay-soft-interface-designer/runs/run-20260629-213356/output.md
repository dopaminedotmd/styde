<!DOCTYPE html>
<html lang=en>
<head>
<meta charset=UTF-8>
<meta name=viewport content="width=device-width,initial-scale=1.0">
<title>Clay Dashboard</title>
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Segoe UI',system-ui,-apple-system,sans-serif;background:#F9F6F2;color:#7D6F5E;padding:24px;min-height:100vh}
.dashboard{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.header{grid-column:1/-1;display:flex;justify-content:space-between;align-items:center;padding:24px 32px;background:#F0EBE3;border-radius:16px;box-shadow:0 8px 32px rgba(0,0,0,0.08)}
.header h1{font-size:24px;font-weight:600;color:#40382E;letter-spacing:-0.3px}
.header p{color:#9C8D7A;font-size:14px;margin-top:2px}
.header-date{text-align:right;font-size:13px;color:#B8AB99}
.card{background:#F0EBE3;border-radius:16px;padding:24px;box-shadow:0 8px 32px rgba(0,0,0,0.06);transition:transform 0.2s,box-shadow 0.2s}
.card:hover{transform:translateY(-2px);box-shadow:0 12px 40px rgba(0,0,0,0.10)}
.card-title{font-size:13px;font-weight:600;color:#9C8D7A;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:12px}
.kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;grid-column:1/-1}
.kpi-card{background:#F0EBE3;border-radius:16px;padding:24px;box-shadow:0 8px 32px rgba(0,0,0,0.06);text-align:center}
.kpi-card:hover{transform:translateY(-2px);box-shadow:0 12px 40px rgba(0,0,0,0.10)}
.kpi-label{font-size:12px;color:#9C8D7A;text-transform:uppercase;letter-spacing:0.4px;margin-bottom:6px}
.kpi-value{font-size:28px;font-weight:700;color:#40382E}
.kpi-change{font-size:12px;margin-top:4px;color:#A8D5A2}
.chart-card{grid-column:span 2}
.bar-chart-wrapper{display:flex;align-items:flex-end;gap:8px;height:180px;padding-top:16px}
.bar{width:100%;border-radius:8px 8px 4px 4px;min-height:8px;transition:opacity 0.2s;position:relative;cursor:pointer}
.bar:hover{opacity:0.8}
.bar:hover::after{content:attr(data-value);position:absolute;top:-28px;left:50%;transform:translateX(-50%);background:#40382E;color:#F9F6F2;font-size:11px;padding:4px 10px;border-radius:8px;white-space:nowrap}
.bar:nth-child(odd){background:#7EC8C0}
.bar:nth-child(even){background:#F4B8A0}
.pie-card{display:flex;flex-direction:column;align-items:center;grid-column:span 1}
.pie-wrapper{position:relative;width:200px;height:200px;margin:12px 0}
.pie{width:100%;height:100%;border-radius:50%;background:conic-gradient(#7EC8C0 0deg 144deg,#F4B8A0 144deg 252deg,#A8D5A2 252deg 324deg,#F0D080 324deg 360deg);box-shadow:0 8px 32px rgba(0,0,0,0.06)}
.pie-center{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:80px;height:80px;border-radius:50%;background:#F0EBE3;display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:inset 0 2px 8px rgba(0,0,0,0.06)}
.pie-center-value{font-size:18px;font-weight:700;color:#40382E}
.pie-center-label{font-size:10px;color:#9C8D7A;text-transform:uppercase;letter-spacing:0.3px}
.legend{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:8px}
.legend-item{display:flex;align-items:center;gap:6px;font-size:11px;color:#7D6F5E}
.legend-dot{width:10px;height:10px;border-radius:4px}
.activity-card{grid-column:1/-1}
.activity-list{display:flex;flex-direction:column;gap:10px}
.activity-row{display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:1px solid #E5DDD0}
.activity-row:last-child{border-bottom:none}
.activity-name{font-size:14px;color:#40382E;font-weight:500}
.activity-meta{font-size:12px;color:#B8AB99}
.status-badge{font-size:11px;padding:4px 12px;border-radius:12px;font-weight:500}
.status-badge.success{background:#A8D5A2;color:#2A241D}
.status-badge.warning{background:#F0D080;color:#2A241D}
@media(max-width:1023px){
.dashboard{grid-template-columns:repeat(2,1fr)}
.kpi-grid{grid-template-columns:repeat(2,1fr)}
.chart-card{grid-column:span 2}
.pie-card{grid-column:span 1}
.pie-wrapper{width:160px;height:160px}
.pie-center{width:64px;height:64px}
}
@media(max-width:767px){
body{padding:12px}
.dashboard{grid-template-columns:1fr;gap:12px}
.header{flex-direction:column;align-items:flex-start;gap:8px;padding:20px}
.kpi-grid{grid-template-columns:1fr 1fr}
.chart-card{grid-column:1}
.pie-card{grid-column:1}
.pie-wrapper{width:120px;height:120px}
.pie-center{width:48px;height:48px}
.pie-center-value{font-size:14px}
.activity-card{grid-column:1}
.bar-chart-wrapper{height:140px}
}
</style>
</head>
<body>
<div class=dashboard>
<div class=header>
<div>
<h1>Studio Overview</h1>
<p>Your creative workspace at a glance</p>
</div>
<div class=header-date>Monday, 29 Jun 2026</div>
</div>
<div class=kpi-grid>
<div class=kpi-card>
<div class=kpi-label>Active Projects</div>
<div class=kpi-value>12</div>
<div class=kpi-change>+2 this week</div>
</div>
<div class=kpi-card>
<div class=kpi-label>Tasks Done</div>
<div class=kpi-value>48</div>
<div class=kpi-change>+8 today</div>
</div>
<div class=kpi-card>
<div class=kpi-label>Team Members</div>
<div class=kpi-value>6</div>
<div class=kpi-change>92% active</div>
</div>
<div class=kpi-card>
<div class=kpi-label>Avg Rating</div>
<div class=kpi-value>4.8</div>
<div class=kpi-change>+0.3 points</div>
</div>
</div>
<div class="card chart-card">
<div class=card-title>Weekly Output</div>
<div class=bar-chart-wrapper>
<div class=bar style=height:60% data-value="1.2k"></div>
<div class=bar style=height:85% data-value="1.8k"></div>
<div class=bar style=height:45% data-value="920"></div>
<div class=bar style=height:95% data-value="2.1k"></div>
<div class=bar style=height:70% data-value="1.5k"></div>
<div class=bar style=height:100% data-value="2.4k"></div>
<div class=bar style=height:55% data-value="1.1k"></div>
<div class=bar style=height:80% data-value="1.7k"></div>
</div>
</div>
<div class="card pie-card">
<div class=card-title>Project Mix</div>
<div class=pie-wrapper>
<div class=pie></div>
<div class=pie-center>
<span class=pie-center-value>40%</span>
<span class=pie-center-label>core</span>
</div>
</div>
<div class=legend>
<div class=legend-item><span class=legend-dot style=background:#7EC8C0></span>Design 40%</div>
<div class=legend-item><span class=legend-dot style=background:#F4B8A0></span>Dev 30%</div>
<div class=legend-item><span class=legend-dot style=background:#A8D5A2></span>Research 20%</div>
<div class=legend-item><span class=legend-dot style=background:#F0D080></span>Ops 10%</div>
</div>
</div>
<div class="card activity-card">
<div class=card-title>Recent Activity</div>
<div class=activity-list>
<div class=activity-row>
<div>
<div class=activity-name>Brand refresh brief</div>
<div class=activity-meta>Due tomorrow</div>
</div>
<span class=status-badge success>on track</span>
</div>
<div class=activity-row>
<div>
<div class=activity-name>User testing session</div>
<div class=activity-meta>3 participants confirmed</div>
</div>
<span class=status-badge success>on track</span>
</div>
<div class=activity-row>
<div>
<div class=activity-name>Component library v2</div>
<div class=activity-meta>12 variants remaining</div>
</div>
<span class=status-badge warning>at risk</span>
</div>
<div class=activity-row>
<div>
<div class=activity-name>Q3 roadmap draft</div>
<div class=activity-meta>Pending review</div>
</div>
<span class=status-badge success>on track</span>
</div>
</div>
</div>
</div>
</body>
</html>