Blueprint: Landing Page Builder
Version: 1
Domain: design
Status: active
landing_page:
  name: Pulse — AI Meeting Scheduler
  goal: free trial signups
  target_audience: busy executives and team leads
  conversion_metric: submit email on hero CTA
structure:
  hero:
    layout: split left-text right-image
    headline: Stop Rescheduling. Start Leading.
    subheadline: Pulse learns your team's availability and auto-negotiates the best meeting time across time zones. No back-and-forth. No double-booking.
    visual: mockup of calendar grid with green checkmarks filling every slot
    primary_cta:
      text: Start Free — No Credit Card
      color: #2563EB
      shape: pill, 48px height
      hover: scale 1.02, shadow lift
    secondary_cta:
      text: Watch 90-Second Demo
      variant: ghost link with play icon
  trust_bar:
    - logo: Forbes / small grayscale
    - logo: TechCrunch / small grayscale
    - logo: Harvard Business Review / small grayscale
    - counter: 12,000+ teams onboarded
  problem_agitation:
    format: two-column pain vs gain
    pain_column:
      icon: clock with red X
      items:
        - 47 minutes wasted per day on scheduling emails
        - 3.2 average reschedules per meeting
        - 4 time-zone slip-ups per week
    gain_column:
      icon: calendar with green check
      items:
        - One-click ideal-time suggestion
        - Auto-reschedule across 12 time zones
        - Integrates with Google / Outlook / Slack
  social_proof:
    type: testimonial carousel
    testimonials:
      - quote: Pulse cut our scheduling overhead by 80%. I got back half my Thursday.
        name: Sarah Chen
        role: VP Engineering, Stripe
        avatar: initials / photo placeholder
      - quote: We onboarded 40 people in 3 minutes. It just works.
        name: Marcus Johansson
        role: Head of Ops, Klarna
        avatar: initials / photo placeholder
      - quote: The time-zone auto-detect alone saved our remote team from disaster.
        name: Aisha Patel
        role: Director of Remote, GitLab
        avatar: initials / photo placeholder
  feature_showcase:
    format: three-card horizontal, icon + headline + one-liner
    features:
      - icon: globe
        headline: Time-Zone Aware
        body: Detects every participant's zone and proposes only valid slots.
      - icon: lightning
        headline: 1-Click Reschedule
        body: Cancel and rebook without re-pinging the whole group.
      - icon: people
        headline: Team Defaults
        body: Set working hours once. Pulse honors them for every member.
  comparison_table:
    type: vs table
    rows:
      - feature: Auto time-zone detection
        pulse: yes
        competitor_avg: partial
      - feature: One-click reschedule
        pulse: yes
        competitor_avg: no
      - feature: Slack native / /pulse command
        pulse: yes
        competitor_avg: no
      - feature: Free tier (up to 5 users)
        pulse: yes
        competitor_avg: yes
      - feature: Recurring meeting optimizer
        pulse: yes
        competitor_avg: limited
  pricing_card:
    variant: single highlight with toggle
    toggle_options: monthly / yearly
    yearly_discount: 20%
    featured_plan:
      name: Pro
      price_monthly: $12/user
      price_yearly: $9/user
      cta: Start 14-Day Free Trial
      features:
        - Unlimited meeting types
        - 12 time-zone support
        - Slack + Teams + Email integrations
        - Analytics dashboard
        - Priority support
  faq:
    - q: Does Pulse work with Google Calendar?
      a: Yes. One-click OAuth sync. Reads existing events to avoid conflicts.
    - q: Can I set different hours for different days?
      a: Yes. Per-day and per-week overrides. Pulse respects them.
    - q: What happens when someone outside my org schedules with me?
      a: They get a link. Pulse detects their time zone automatically. They see only valid slots.
    - q: Is there a free plan?
      a: Yes. Up to 5 users, unlimited meetings. No credit card required.
  footer_cta:
    headline: Your calendar should work for you, not against you.
    subheadline: Join 12,000+ teams who stopped fighting the clock.
    cta: Claim Your Free Account
    microcopy: No credit card. Cancel anytime.
mobile_optimizations:
  - stack hero vertically: headline -> subheadline -> image -> cta
  - collapse feature cards to single column
  - testimonial carousel becomes swipeable full-width cards
  - comparison table becomes horizontal scroll or stacked list
  - cta button full-width, minimum 48px touch target
  - faq accordion with tap-to-expand
copy_tone:
  style: direct, benefit-first, executive
  pronouns: you / your (address reader directly)
  active_verbs: stop, start, save, reclaim, eliminate
  social_currency: mention Stripe, Klarna, GitLab as existing users
a_b_test_recommendations:
  - test: hero headline
    variant_a: Stop Rescheduling. Start Leading.
    variant_b: Save 47 Minutes a Day on Scheduling. Free.
    expected_winner: b (more concrete number)
  - test: cta color
    variant_a: blue #2563EB
    variant_b: green #059669
    expected_winner: green (higher click-through in scheduling context)
  - test: pricing toggle default
    variant_a: yearly pre-selected (shows discounted price)
    variant_b: monthly pre-selected
    expected_winner: yearly pre-selected (anchor effect)
technical_notes:
  - hero image lazy-loaded with blur placeholder
  - testimonial carousel pauses on hover
  - faq uses schema.org/FAQPage structured data
  - cta button sends event to GA4 and HubSpot
  - form fields: email only (single field for hero CTA)
  - thank-you redirect under 200ms after submit