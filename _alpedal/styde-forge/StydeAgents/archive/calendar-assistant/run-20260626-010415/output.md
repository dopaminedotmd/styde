status: ready
mode: natural-language-scheduling
capabilities:
  - book
  - reschedule
  - cancel
  - recurring-series
  - preference-learning
inputs_expected:
  - event_name
  - date_or_range
  - duration
  - attendees
  - time_preference: morning|afternoon|flexible
  - recurrence: daily|weekly|biweekly|monthly|none
processing:
  1. parse_request
  2. check_calendar_for_conflicts
  3. apply_preferences_and_buffer
  4. confirm_slot
  5. return_booking_ref
example:
  input: schedule a 30-min standup tomorrow morning with the team
  output:
    action: booked
    event: Daily Standup
    date: 2026-06-27
    time: "09:00-09:30"
    attendees: team
    ref: CAL-20260627-001
    conflicts: none
    buffer_applied: 5min post
Awaiting your scheduling request.