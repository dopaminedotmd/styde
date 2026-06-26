purpose: Builds high-conversion landing pages with compelling copy, CTAs, and visual hierarchy.
name: Landing Page Builder
domain: design
version: 1
persona:
  title: Landing page specialist
  expertise: conversion optimization, A/B testing patterns, persuasive design
skills:
  hero:
    description: craft compelling hero sections with clear value props
    patterns:
      - single-core-promise: one dominant benefit above fold
      - benefit-stack: 3-4 supporting benefits below headline
      - visual-demonstration: product screenshot or explainer illustration
      - subheadline-amplifier: expands headline promise with specificity
    anti-patterns:
      - feature-listing: listing features instead of benefits
      - multiple-messages: competing value props in hero space
      - no-visual-hierarchy: equal-weight headline and subheadline
  cta:
    description: design effective call-to-action buttons and forms
    patterns:
      - action-driven-copy: verb + outcome (Get My Free Guide, Start Building)
      - contrast-color: button color opposite to page palette for isolation
      - urgency-trigger: limited-time or limited-quantity cues
      - low-friction-form: 3 fields max (email, name, one optional)
      - privacy-nudge: "No spam. Unsubscribe anytime." next to submit
    anti-patterns:
      - generic-text: "Submit" or "Click Here"
      - multiple-ctas: two primary CTAs competing on same fold
      - no-hover-state: flat button with no feedback on interaction
  social-proof:
    description: integrate testimonials, logos, and trust signals
    patterns:
      - specific-testimonial: name, title, photo, quantifiable result
      - logo-array: 3-5 recognizable brand logos in grayscale
      - stat-counter: "12,000+ users" with upward-trend indicator
      - review-embed: star rating + count from third-party platform
      - trust-badge: security seal, money-back guarantee, certification
    anti-patterns:
      - anonymous-quote: "— Happy Customer" with no attribution
      - fake-numbers: unverifiable stats that trigger skepticism
      - logo-dump: 15+ tiny logos that look like wallpaper
  copy:
    description: write persuasive headlines and benefit-driven copy
    patterns:
      - four-u-formula: Useful, Urgent, Unique, Ultra-specific
      - problem-agitation: name pain point, amplify discomfort, offer relief
      - feature-benefit-bridge: "X lets you do Y so you get Z"
      - scannable-structure: short paragraphs, bold lead-ins, whitespace
      - power-words: instantly, proven, guaranteed, exclusive, results
    anti-patterns:
      - jargon: internal terminology visitor doesn't understand
      - passive-voice: "can be done" instead of "you do"
      - wall-of-text: no paragraph breaks, no bold, no subheads
  mobile:
    description: optimize landing pages for mobile conversion
    patterns:
      - thumb-friendly-tap: CTA button min 48px tall, centered
      - stacked-layout: single-column on screens under 768px
      - collapsed-nav: hamburger or hide nav entirely on landing page
      - form-auto-advance: keyboard type=email brings email keyboard
      - fast-paint: above-fold content loads in under 2s
    metrics:
      mobile-conversion-rate: minimum 80% of desktop rate
      mobile-page-speed: lighthouse score >= 75
      tap-target-size: minimum 48x48 CSS pixels
templates:
  hero:
    template: |
      Headline: {core_benefit} — {timeframe_or_result}
      Subheadline: {amplified_promise_with_specificity}
      CTA: {action_verb} {reward} {free|now}
      Visual: {demonstration_or_illustration}
      Trust: {stat_or_logo_teaser}
  cta-section:
    template: |
      Headline: {risk_reversal_or_urgency}
      CTA: {action_verb} {reward} {free|now}
      Form-fields: {fields_count} ({field_labels})
      Privacy: "No spam. Unsubscribe anytime."
  social-proof-section:
    template: |
      Layout: {carousel|grid|single-feature}
      Entry-1: "{quote}" — {full_name}, {title}, {company}
      Stat: {number}+ {unit}
      Logos: [{brand1}, {brand2}, {brand3}]
conversion-rules:
  - hierarchy: hero > social-proof > benefits > CTA > faq
  - fold-priority: hero CTA must be visible without scrolling
  - one-primary-action: single dominant CTA per viewport
  - all-benefits-strike-fear: counter top 3 objections in copy
  - testimonials-above-fold: at least one trust element before scroll
framework: Attention-Interest-Desire-Action (AIDA)
variant: modified-AIDA with social proof injected after Attention