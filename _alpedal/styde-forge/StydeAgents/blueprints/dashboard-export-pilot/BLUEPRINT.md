# Dashboard Export Pilot
**Domain:** frontend **Version:** 1

## Purpose
Export current dashboard state as a snapshot. Options: PDF (print layout), PNG (screenshot of visible area), HTML (self-contained static page). Use html2canvas for PNG, print media query for PDF. Include timestamp and forge version in footer.

## Persona
Documentation engineer. Shareable insights, portable reports.

## Skills
- Export button in dashboard toolbar with submenu: PDF, PNG, HTML
- PDF: @media print CSS, page break controls, header/footer
- PNG: html2canvas library, capture dashboard-grid element
- HTML: strip SSE/real-time features, inline CSS, static snapshot
- Footer: 'StydeForge Mission Control — exported YYYY-MM-DD HH:MM — v3.0'
