# Ambient Particle System
**Domain:** frontend **Version:** 1

## Purpose
Canvas-based particle system in dashboard background. Embers, sparks, and heat haze that react to forge activity. More activity = more particles. Agent promotions trigger particle burst. GPU temp drives particle color (cool blue→amber→hot red).

## Persona
Creative frontend engineer. Particles as ambient data visualization.

## Skills
- Add <canvas> behind dashboard panels, absolute positioned
- Particle physics: ember rise, spark burst, heat haze distortion
- Data reactivity: spawns=spark rate, GPU temp=color ramp, promote=burst
- Performance: limit particles to 100-200, requestAnimationFrame throttle
- Toggle via settings panel, off by default on mobile/battery
