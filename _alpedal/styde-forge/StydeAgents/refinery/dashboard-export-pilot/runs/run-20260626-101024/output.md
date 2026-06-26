Export feature already fully implemented in live-collab-canvas.html. All 5 spec items verified in current code:
item: Export button with submenu
status: PRESENT
location: line 193-200
details: #export-btn in .topbar-actions with .export-wrapper dropdown containing PDF/PNG/HTML options, click-to-toggle with close-on-outside-click (line 1372-1382)
item: PDF export
status: PRESENT
location: lines 158-178, 1274-1278
details: @media print with landscape, 12mm margins, page-break-inside:avoid on .panel and #grid, page-break-inside:avoid on .panel-body. #print-header and #print-footer injected before calling window.print(). Non-print elements (#topbar, #filter-bar, #chat-sidebar, #comment-panel, #follow-banner, #connection-status, .panel-status-bar, .lock-btn, .comment-btn) hidden with display:none. Canvas max-height 220px.
item: PNG export
status: PRESENT
location: lines 1280-1312
details: html2canvas loaded from CDN (line 180). Captures #grid element at 2x scale, backgroundColor #0f1117, useCORS:true. Footer rendered onto canvas via 2D context overlay (fillRect + fillText at bottom-center). Downloads as stydeforge-dashboard-<timestamp>.png.
item: HTML export
status: PRESENT
location: lines 1315-1369
details: DOM clone with script stripping - removes all scripts except html2canvas, removes scripts containing BroadcastChannel/channel/cursor/follow/initWS. Removes connection-status, sync-badge, follow elements, status-dot, filter-lock. Strips chat/comment/annotation/toast elements except chat-sidebar container. Inlines CSS minus @media print rules. Adds static snapshot override styles for export button visibility. Header/footer displayed statically. Downloads as stydeforge-dashboard-<timestamp>.html.
item: Footer format
status: PRESENT
location: lines 1266-1272
details: getFooterText() returns 'StydeForge Mission Control --- exported YYYY-MM-DD HH:MM --- v3.0'
No implementation needed. Feature complete and production-ready with error handling (html2canvas missing check, catch blocks on PNG, toast notifications for success/failure per format).