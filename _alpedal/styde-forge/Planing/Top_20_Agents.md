# Top 20 Agents — Styde Forge World-Class Priority Queue

**Created:** 2026-06-25
**Purpose:** First 20 agents for the Styde Forge refinery. Ordered by business impact × forge-optimization potential.

---

## Tier 1 — Revenue Generators (Build First)

### 1. Consultant Auditor
Crawls company website + public data → classifies digital maturity → generates structured audit report.
- **Forge boost:** Eval loop improves classification accuracy over time. Pattern library grows with each audit.
- **Customer value:** Immediate. This IS the sales hook. "We ran our AI on your website. Here's what we found."
- **Benchmark:** audit-accuracy (known companies with pre-scored maturity)

### 2. Invoice Processor
Reads invoice PDFs → extracts line items, amounts, dates, VAT → outputs structured JSON for accounting.
- **Forge boost:** Extraction accuracy improves per industry. Edge cases (handwritten, multi-page, foreign currencies) trained through eval.
- **Customer value:** 5-15 hours/week saved per SME. Direct cost reduction.
- **Benchmark:** invoice-extraction-accuracy (known invoices with ground truth)

### 3. Customer Service Triage
Reads incoming email/chat → classifies urgency + topic → drafts response or routes to human.
- **Forge boost:** Classification accuracy + response quality improve. Tone adapts per customer.
- **Customer value:** First response time drops from hours to seconds. Human handles complex only.
- **Benchmark:** triage-accuracy + response-quality (human-rated)

### 4. Meeting Summary Generator
Takes meeting transcript → extracts decisions, action items, owners, deadlines → structured summary.
- **Forge boost:** Extraction precision improves. Learns company-specific terminology.
- **Customer value:** Zero post-meeting admin. Actions tracked automatically.
- **Benchmark:** summary-completeness (human-rated against known transcript)

### 5. Email Drafter
Given context (previous thread, company knowledge) → drafts professional email in correct tone.
- **Forge boost:** Tone adaptation. Learns per-user style preferences.
- **Customer value:** 2-5 hours/week saved. Consistent communication quality.
- **Benchmark:** email-quality (human-rated: correctness, tone, completeness)

---

## Tier 2 — Efficiency Multipliers

### 6. Document Classifier
Reads any document → classifies type (invoice, contract, report, CV, etc.) → routes to correct handler.
- **Forge boost:** Type coverage expands. Confidence thresholds tighten.
- **Customer value:** End of manual document sorting. Foundation for all document workflows.
- **Benchmark:** classification-accuracy (known document set)

### 7. Contract Reviewer
Reads contract → identifies key clauses (termination, liability, payment terms, GDPR) → flags risks.
- **Forge boost:** Risk detection improves. Clause library grows per industry.
- **Customer value:** Legal review time cut by 70%. Risks caught before signing.
- **Benchmark:** clause-detection-accuracy (lawyer-annotated contracts)

### 8. Report Writer
Given structured data + template → writes polished business report (monthly, quarterly, project).
- **Forge boost:** Quality improves per report type. Learns company voice.
- **Customer value:** Reports that took 4 hours take 15 minutes.
- **Benchmark:** report-quality (human-rated: accuracy, clarity, completeness)

### 9. Data Cleaner
Reads messy spreadsheet → identifies duplicates, formatting errors, missing values → cleans + reports what was fixed.
- **Forge boost:** Error pattern detection improves. Learns per-industry data shapes.
- **Customer value:** Hours of manual Excel work eliminated.
- **Benchmark:** cleaning-accuracy (pre-scored messy datasets)

### 10. Calendar Assistant
Given natural language request → finds available slots, books meetings, sends invites, handles reschedules.
- **Forge boost:** Scheduling logic improves. Learns per-person preferences (morning vs afternoon, length).
- **Customer value:** 1-2 hours/week saved. No back-and-forth emails.
- **Benchmark:** scheduling-accuracy (correct slot found, no conflicts)

---

## Tier 3 — Capability Builders

### 11. Code Reviewer
Reviews code → finds bugs, security issues, style violations → suggests fixes.
- **Forge boost:** Bug detection rate improves. Language coverage expands.
- **Customer value:** Internal dev teams ship faster with fewer bugs.
- **Benchmark:** code-review-basic (known bugs in test files)

### 12. SQL Query Generator
Given natural language question + schema → generates correct SQL query with explanation.
- **Forge boost:** Query correctness improves. Schema understanding deepens.
- **Customer value:** Non-technical staff query databases without SQL knowledge.
- **Benchmark:** query-accuracy (known question → answer pairs)

### 13. Translator (Business Swedish ↔ English)
Translates business documents maintaining tone, terminology, and legal precision.
- **Forge boost:** Domain terminology accuracy improves. Learns per-company glossary.
- **Customer value:** Swedish SMEs communicating internationally. Critical for export businesses.
- **Benchmark:** translation-quality (bilingual human-rated)

### 14. Social Media Writer
Given company news/update → writes platform-optimized posts (LinkedIn, Instagram, Twitter).
- **Forge boost:** Engagement prediction improves. Learns per-platform best practices.
- **Customer value:** Consistent social presence without dedicated staff.
- **Benchmark:** post-quality (human-rated: engagement potential, brand consistency)

### 15. Onboarding Guide
Given new employee role + company handbook → generates personalized onboarding plan with tasks, reading, and checkpoints.
- **Forge boost:** Plan quality improves. Learns per-role requirements.
- **Customer value:** Structured onboarding without HR manually creating plans.
- **Benchmark:** plan-completeness (HR-rated)

---

## Tier 4 — Specialized Agents

### 16. GDPR Compliance Checker
Reads privacy policy / data handling docs → checks against GDPR requirements → flags gaps with specific article references.
- **Forge boost:** Detection coverage expands. Learns per-industry regulation nuances.
- **Customer value:** GDPR audit prep in hours instead of weeks. Critical for Swedish companies.
- **Benchmark:** gdpr-detection-accuracy (lawyer-annotated policies)

### 17. Inventory Forecaster
Given sales history → predicts stock needs for next 30/60/90 days with confidence intervals.
- **Forge boost:** Forecast accuracy improves per product category. Learns seasonality patterns.
- **Customer value:** Reduced stockouts. Reduced overstock. Direct margin impact.
- **Benchmark:** forecast-accuracy (known historical → actual data)

### 18. Recruitment Screener
Reads CVs + job description → ranks candidates with reasoning → drafts screening questions.
- **Forge boost:** Ranking accuracy improves. Learns per-role success patterns.
- **Customer value:** 50 CVs → top 5 in minutes. Hiring manager focuses on best candidates.
- **Benchmark:** screening-accuracy (recruiter-rated rankings)

### 19. Competitor Monitor
Monitors competitor websites + news → detects changes (pricing, features, hiring) → weekly brief.
- **Forge boost:** Signal-to-noise ratio improves. Learns what changes matter per industry.
- **Customer value:** Competitive intelligence without manual monitoring.
- **Benchmark:** brief-quality (human-rated: relevance, accuracy, timeliness)

### 20. Meta-Improver (Forge Self-Improvement)
Analyzes Forge eval results → identifies systemic weaknesses → proposes blueprint improvements.
- **Forge boost:** This IS the self-improvement engine. Makes all other agents better.
- **Customer value:** Indirect but exponential. Every agent gets better every iteration.
- **Benchmark:** meta-basic (proposal quality: specific, quantified, testable)

---

## Build Order Strategy

```
WEEK 1-2:   #1 Consultant Auditor (sales enablement)
            #5 Email Drafter (quick win, immediate value)

WEEK 3-4:   #2 Invoice Processor (revenue: direct cost savings)
            #3 Customer Service Triage (broad applicability)

WEEK 5-6:   #6 Document Classifier (foundation for #7, #16)
            #10 Calendar Assistant (universal need)

WEEK 7-8:   #4 Meeting Summarizer
            #8 Report Writer
            #7 Contract Reviewer

WEEK 9-10:  #16 GDPR Checker (Swedish market requirement)
            #14 Social Media Writer

WEEK 11-12: #11 Code Reviewer (internal use first)
            #20 Meta-Improver (start the self-improvement loop)

WEEK 13+:   Remaining agents in priority order
```

---

## Why This Order?

| Agent | Why Now |
|-------|---------|
| Consultant Auditor | Sales hook. Nothing else matters without customers. |
| Email Drafter | Universal pain point. Quick to build. Shows immediate value. |
| Invoice Processor | Concrete ROI (hours saved × hourly rate). Easy to sell. |
| Customer Service Triage | Every company has customer service. Broad market. |
| Document Classifier | Foundation agent — other agents (#7, #16) depend on it. |
| Meta-Improver | Starts the exponential curve. Every iteration makes ALL agents better. |

---

**Status:** 20 agents defined. Build order prioritized by revenue impact.
