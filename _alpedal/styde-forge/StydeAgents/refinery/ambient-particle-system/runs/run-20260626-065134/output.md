The ambient particle system is already fully implemented inside dashboard.py.
status: COMPLETE
file: D:\styde\_alpedal\styde-forge\Core\dashboard.py
Current implementation details:
- Canvas at line 470, styled fixed/inset:0/z-index:0/pointer-events:none
- Particle engine at lines 764-946 inside the fallback HTML template
- 3 particle types: ember (rise+glow), spark (fast burst trails), haze (slow heat distortion)
- GPU temp drives particle color ramp: 40-140-200 (cool blue) to 240-20-20 (hot red) via _lastGpuTemp
- Spawn rate driven by _lastSpawned: rate = min(spawned/10, 3) particles per frame
- burstPromote() triggers on agent promotion -- 30 sparks + 12 haze ring + 8 ember ring, called from line 690
- MAX_PARTICLES=180, requestAnimationFrame loop with dt clamping at 50ms
- Toggle via particles button at line 557 in control tab, state persisted in localStorage
- Mobile/battery detection: off by default on mobile UA, on battery without charging
- DPR-aware canvas scaling
- CSS class .active transitions opacity 0->1 over 1s
No external Dashboard/mission-control.html exists, so the fallback inline HTML runs.