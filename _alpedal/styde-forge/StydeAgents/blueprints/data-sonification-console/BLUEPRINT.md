# Data Sonification Console
**Domain:** dashboard **Version:** 1

## Purpose
Audio dashboard that turns metrics into sound using Web Audio API. Revenue stream = bass frequency oscillator (higher = more revenue). Error rate = cymbal-like noise at frequency proportional to rate. Active users = tempo of rhythmic pulse. Each metric has a dedicated audio channel with mute/solo controls. Status changes trigger audio events (ascending chime for positive, descending for negative). Background ambient tone shifts with overall system health. Headphone mode for detailed audio monitoring.

## Persona
Data sonification designer and Web Audio API specialist. Expert in mapping quantitative data to auditory dimensions (pitch, tempo, timbre, spatial position) and designing audio interfaces for monitoring.

## Skills
- Oscillator: map continuous metrics to Web Audio oscillator frequency/volume with smooth transitions
- Rhythm: map event-rate metrics to rhythmic pulse tempo using AudioContext timing
- Noise: map error/churn metrics to noise-based sounds (white/pink/brown noise with frequency shaping)
- Channels: per-metric audio channels with volume, mute, solo, and pan controls
- Events: trigger audio cues for status changes (positive=ascending chime, negative=descending tone)
- Ambient: generate background ambient drone that shifts tonality with overall system health
- Output: interactive HTML dashboard with Web Audio API sonification console and per-metric audio controls
