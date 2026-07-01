AmbientParticleSystem.js
```javascript
const PARTICLE_LIMIT = { MIN: 100, MAX: 200 }
const SPAWN_RATE = { IDLE: 0.3, ACTIVE: 2, BURST: 20 }
const TEMP_RAMP = { COOL: 0.3, WARM: 0.6, HOT: 0.9 }
class Particle {
  constructor(x, y, type) {
    this.x = x
    this.y = y
    this.type = type // ember | spark | haze
    this.vx = 0
    this.vy = 0
    this.life = 1
    this.decay = 0.005 + Math.random() * 0.015
    this.size = 0
    this.color = { r: 255, g: 200, b: 100, a: 1 }
    this.burst = false
    this.init(type)
  }
  init(type) {
    switch (type) {
      case 'ember':
        this.size = 1.5 + Math.random() * 2
        this.vy = -(0.3 + Math.random() * 0.8)
        this.vx = (Math.random() - 0.5) * 0.5
        this.decay = 0.003 + Math.random() * 0.008
        this.color = { r: 255, g: 150 + Math.random() * 80, b: 50, a: 0.8 }
        break
      case 'spark':
        this.size = 0.5 + Math.random() * 1
        this.vy = -(0.8 + Math.random() * 1.5)
        this.vx = (Math.random() - 0.5) * 1.5
        this.decay = 0.01 + Math.random() * 0.025
        this.color = { r: 255, g: 220 + Math.random() * 35, b: 100 + Math.random() * 80, a: 1 }
        break
      case 'haze':
        this.size = 8 + Math.random() * 20
        this.vy = -(0.05 + Math.random() * 0.1)
        this.vx = (Math.random() - 0.5) * 0.2
        this.decay = 0.001 + Math.random() * 0.003
        this.color = { r: 200, g: 120, b: 60, a: 0.05 + Math.random() * 0.08 }
        break
    }
  }
  update(gpuTemp, dt) {
    this.x += this.vx * dt
    this.y += this.vy * dt
    this.life -= this.decay * dt
    if (this.type === 'ember') {
      this.vx += (Math.random() - 0.5) * 0.1 * dt
      this.size *= 0.998
    }
    if (this.type === 'spark' && this.burst) {
      this.vx *= 0.97
      this.vy *= 0.97
    }
    this.applyTempColor(gpuTemp)
    return this.life > 0
  }
  applyTempColor(gpuTemp) {
    const t = Math.min(1, Math.max(0, gpuTemp))
    let r, g, b
    if (t < TEMP_RAMP.COOL) {
      const p = t / TEMP_RAMP.COOL
      r = Math.round(100 + p * 155)
      g = Math.round(150 + p * 105)
      b = Math.round(255 - p * 155)
    } else if (t < TEMP_RAMP.WARM) {
      const p = (t - TEMP_RAMP.COOL) / (TEMP_RAMP.WARM - TEMP_RAMP.COOL)
      r = Math.round(255)
      g = Math.round(255 - p * 105)
      b = Math.round(100 - p * 50)
    } else {
      const p = (t - TEMP_RAMP.WARM) / (TEMP_RAMP.HOT - TEMP_RAMP.WARM)
      r = Math.round(255)
      g = Math.round(150 - p * 100)
      b = Math.round(50 - p * 30)
    }
    this.color.r = r
    this.color.g = g
    this.color.b = b
  }
  draw(ctx) {
    const a = this.color.a * this.life
    if (a < 0.01) return
    ctx.save()
    ctx.globalAlpha = a
    switch (this.type) {
      case 'haze':
        ctx.filter = `blur(${this.size * 0.4}px)`
        ctx.fillStyle = `rgba(${this.color.r},${this.color.g},${this.color.b},${a * 0.15})`
        ctx.beginPath()
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2)
        ctx.fill()
        ctx.filter = 'none'
        break
      case 'spark':
        ctx.shadowColor = `rgba(${this.color.r},${this.color.g},${this.color.b},${a})`
        ctx.shadowBlur = 6
        ctx.fillStyle = `rgba(${this.color.r},${this.color.g},${this.color.b},${a})`
        ctx.beginPath()
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2)
        ctx.fill()
        break
      case 'ember':
        ctx.shadowColor = `rgba(255,${this.color.g},${this.color.b},${a * 0.5})`
        ctx.shadowBlur = 4
        ctx.fillStyle = `rgba(${this.color.r},${this.color.g},${this.color.b},${a})`
        ctx.beginPath()
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2)
        ctx.fill()
        this.drawGlow(ctx, a)
        break
    }
    ctx.restore()
  }
  drawGlow(ctx, a) {
    const grad = ctx.createRadialGradient(
      this.x, this.y, 0,
      this.x, this.y, this.size * 3
    )
    grad.addColorStop(0, `rgba(255,${this.color.g - 50},${this.color.b - 30},${a * 0.3})`)
    grad.addColorStop(1, `rgba(255,${this.color.g - 50},${this.color.b - 30},0)`)
    ctx.fillStyle = grad
    ctx.beginPath()
    ctx.arc(this.x, this.y, this.size * 3, 0, Math.PI * 2)
    ctx.fill()
  }
}
class AmbientParticleSystem {
  constructor(canvas, options = {}) {
    this.canvas = canvas
    this.ctx = canvas.getContext('2d')
    this.particles = []
    this.running = false
    this.rafId = null
    this.lastFrame = 0
    this.options = {
      maxParticles: PARTICLE_LIMIT.MAX,
      spawnRate: SPAWN_RATE.IDLE,
      gpuTemp: 0.3,
      burstActive: false,
      burstCount: 0,
      enabled: true,
      ...options
    }
    this.metrics = { spawns: 0, deaths: 0, burstEvents: 0 }
    this.handleResize = this.handleResize.bind(this)
    this.loop = this.loop.bind(this)
  }
  get forgeActivityRate() {
    return this.options.spawnRate
  }
  set forgeActivityRate(val) {
    this.options.spawnRate = Math.max(SPAWN_RATE.IDLE, Math.min(SPAWN_RATE.ACTIVE, val))
  }
  get gpuTemp() {
    return this.options.gpuTemp
  }
  set gpuTemp(val) {
    this.options.gpuTemp = Math.max(0, Math.min(1, val))
  }
  start() {
    if (this.running) return
    this.running = true
    this.resize()
    window.addEventListener('resize', this.handleResize)
    this.lastFrame = performance.now()
    this.loop(this.lastFrame)
  }
  stop() {
    this.running = false
    if (this.rafId) {
      cancelAnimationFrame(this.rafId)
      this.rafId = null
    }
    window.removeEventListener('resize', this.handleResize)
    this.clear()
  }
  toggle(force) {
    this.options.enabled = force !== undefined ? force : !this.options.enabled
    if (this.options.enabled) {
      this.start()
    } else {
      this.stop()
    }
    return this.options.enabled
  }
  resize() {
    const rect = this.canvas.parentElement.getBoundingClientRect()
    this.canvas.width = rect.width * devicePixelRatio
    this.canvas.height = rect.height * devicePixelRatio
    this.canvas.style.width = rect.width + 'px'
    this.canvas.style.height = rect.height + 'px'
    this.ctx.scale(devicePixelRatio, devicePixelRatio)
  }
  handleResize() {
    this.resize()
  }
  triggerBurst(count = 30) {
    if (!this.options.enabled || !this.running) return
    this.metrics.burstEvents++
    this.options.burstActive = true
    this.options.burstCount = count
    for (let i = 0; i < count; i++) {
      if (this.particles.length >= PARTICLE_LIMIT.MAX) break
      const w = this.canvas.width / devicePixelRatio
      const h = this.canvas.height / devicePixelRatio
      const x = w * 0.2 + Math.random() * w * 0.6
      const y = h * 0.6 + Math.random() * h * 0.35
      const p = new Particle(x, y, 'spark')
      p.burst = true
      p.vy = -(2 + Math.random() * 4)
      p.vx = (Math.random() - 0.5) * 6
      this.particles.push(p)
    }
  }
  spawn(rate) {
    const effectiveMax = PARTICLE_LIMIT.MIN +
      Math.round((PARTICLE_LIMIT.MAX - PARTICLE_LIMIT.MIN) * this.options.spawnRate / SPAWN_RATE.ACTIVE)
    if (this.particles.length >= effectiveMax) return
    const shouldSpawn = rate > 1 ? rate : Math.random() < rate
    if (!shouldSpawn) return
    this.metrics.spawns++
    const w = this.canvas.width / devicePixelRatio
    const h = this.canvas.height / devicePixelRatio
    const x = Math.random() * w
    const y = h + 10
    let type = 'ember'
    if (this.options.spawnRate > SPAWN_RATE.IDLE * 2 && Math.random() < 0.2) {
      type = 'spark'
    }
    if (Math.random() < 0.05) {
      type = 'haze'
    }
    this.particles.push(new Particle(x, y, type))
  }
  clear() {
    this.particles = []
  }
  loop(timestamp) {
    if (!this.running) return
    const dt = Math.min((timestamp - this.lastFrame) / 16.67, 3)
    this.lastFrame = timestamp
    const ctx = this.ctx
    const w = this.canvas.width / devicePixelRatio
    const h = this.canvas.height / devicePixelRatio
    ctx.clearRect(0, 0, w, h)
    this.spawn(this.options.spawnRate)
    if (this.options.burstActive && this.options.burstCount > 0) {
      this.options.burstCount--
      if (this.options.burstCount <= 0) {
        this.options.burstActive = false
      }
    }
    let newParticles = []
    for (const p of this.particles) {
      if (p.update(this.options.gpuTemp, dt)) {
        newParticles.push(p)
      } else {
        this.metrics.deaths++
      }
    }
    this.particles = newParticles
    for (const p of this.particles) {
      p.draw(ctx)
    }
    this.rafId = requestAnimationFrame(this.loop)
  }
  destroy() {
    this.stop()
    this.canvas = null
    this.ctx = null
  }
}
export { AmbientParticleSystem, Particle, SPAWN_RATE, PARTICLE_LIMIT, TEMP_RAMP }
```
useAmbientParticles.js
```javascript
import { useEffect, useRef, useCallback, useMemo } from 'react'
import { AmbientParticleSystem, SPAWN_RATE } from './AmbientParticleSystem'
function getBatterySafe() {
  if (typeof navigator === 'undefined' || !navigator.getBattery) return Promise.resolve(null)
  return navigator.getBattery().catch(() => null)
}
function getDeviceProfile() {
  const ua = navigator.userAgent || ''
  const isMobile = /Android|iPhone|iPad|iPod|webOS|BlackBerry|IEMobile|Opera Mini/i.test(ua)
  const isTablet = /iPad|Android(?!.*Mobile)|Tablet/i.test(ua)
  const isLowPower = navigator.hardwareConcurrency <= 4 || 'deviceMemory' in navigator && navigator.deviceMemory <= 4
  return { isMobile, isTablet, isLowPower }
}
export function useAmbientParticles(options = {}) {
  const canvasRef = useRef(null)
  const systemRef = useRef(null)
  const settingsRef = useRef({
    enabled: options.defaultEnabled !== undefined ? options.defaultEnabled : true,
    batteryDetectMethod: options.batteryDetectMethod !== undefined ? options.batteryDetectMethod : 'getBattery',
    throttleInterval: options.throttleInterval || 1000,
    forgeActivitySource: options.forgeActivitySource || null,
    gpuTempSource: options.gpuTempSource || null,
    promoteSource: options.promoteSource || null
  })
  const init = useCallback(async () => {
    const canvas = canvasRef.current
    if (!canvas) return null
    const profile = getDeviceProfile()
    const settings = settingsRef.current
    if (profile.isMobile && !settings.enabled) {
      return null
    }
    if (profile.isLowPower || profile.isMobile) {
      settings.maxParticles = 100
    }
    if (settings.batteryDetectMethod === 'getBattery') {
      try {
        const battery = await getBatterySafe()
        if (battery && battery.level <= 0.2) {
          return null
        }
      } catch (e) {
      }
    }
    const system = new AmbientParticleSystem(canvas, {
      maxParticles: options.maxParticles || (profile.isMobile ? 100 : 200),
      spawnRate: SPAWN_RATE.IDLE
    })
    systemRef.current = system
    system.start()
    return system
  }, [options.maxParticles, options.defaultEnabled, options.batteryDetectMethod])
  useEffect(() => {
    let mounted = true
    let activityInterval = null
    let tempInterval = null
    let promoteHandler = null
    let initPromise = init()
    initPromise.then(system => {
      if (!mounted || !system) return
      const settings = settingsRef.current
      if (settings.forgeActivitySource) {
        activityInterval = setInterval(() => {
          if (!system.running) return
          let rate = SPAWN_RATE.IDLE
          if (typeof settings.forgeActivitySource === 'function') {
            try {
              const val = settings.forgeActivitySource()
              if (typeof val === 'number') rate = Math.max(SPAWN_RATE.IDLE, Math.min(SPAWN_RATE.ACTIVE, val))
            } catch (e) {}
          }
          system.forgeActivityRate = rate
        }, settings.throttleInterval)
      }
      if (settings.gpuTempSource) {
        tempInterval = setInterval(() => {
          if (!system.running) return
          if (typeof settings.gpuTempSource === 'function') {
            try {
              const val = settings.gpuTempSource()
              if (typeof val === 'number') system.gpuTemp = val
            } catch (e) {}
          }
        }, settings.throttleInterval)
      }
      if (settings.promoteSource) {
        if (typeof settings.promoteSource === 'function') {
          promoteHandler = () => {
            if (!system.running) return
            system.triggerBurst(30)
          }
          const sub = settings.promoteSource(promoteHandler)
          if (sub && typeof sub.unsubscribe === 'function') {
            promoteHandler = sub
          }
        } else if (settings.promoteSource && typeof settings.promoteSource.addEventListener === 'function') {
          promoteHandler = () => system.triggerBurst(30)
          settings.promoteSource.addEventListener('promote', promoteHandler)
        }
      }
    })
    return () => {
      mounted = false
      if (activityInterval) clearInterval(activityInterval)
      if (tempInterval) clearInterval(tempInterval)
      if (promoteHandler) {
        const settings = settingsRef.current
        if (settings.promoteSource && typeof settings.promoteSource.removeEventListener === 'function') {
          settings.promoteSource.removeEventListener('promote', promoteHandler)
        }
      }
      if (systemRef.current) {
        systemRef.current.destroy()
        systemRef.current = null
      }
    }
  }, [init])
  const setEnabled = useCallback((val) => {
    if (systemRef.current) {
      return systemRef.current.toggle(val)
    }
    settingsRef.current.enabled = val
    return val
  }, [])
  const triggerBurst = useCallback((count = 30) => {
    if (systemRef.current) {
      systemRef.current.triggerBurst(count)
    }
  }, [])
  return {
    canvasRef,
    setEnabled,
    triggerBurst,
    isRunning: () => systemRef.current ? systemRef.current.running : false,
    getMetrics: () => systemRef.current ? systemRef.current.metrics : null
  }
}
```
AmbientParticlePanel.jsx
```javascript
import React, { useEffect, useRef, useCallback, useState } from 'react'
import { useAmbientParticles } from './useAmbientParticles'
function AmbientParticlePanel({ 
  className,
  style,
  forgeActivitySource,
  gpuTempSource,
  promoteSource,
  defaultEnabled = true,
  throttleInterval = 1000,
  batteryDetectMethod = 'getBattery',
  children
}) {
  const containerRef = useRef(null)
  const [visible, setVisible] = useState(defaultEnabled)
  const [metrics, setMetrics] = useState(null)
  const { canvasRef, setEnabled, triggerBurst } = useAmbientParticles({
    defaultEnabled,
    batteryDetectMethod,
    throttleInterval,
    forgeActivitySource,
    gpuTempSource,
    promoteSource
  })
  const toggleParticles = useCallback((val) => {
    const state = setEnabled(val)
    setVisible(state)
  }, [setEnabled])
  useEffect(() => {
    const interval = setInterval(() => {
      if (canvasRef.current && canvasRef.current.getContext) {
        setMetrics({ count: 0 })
      }
    }, 2000)
    return () => clearInterval(interval)
  }, [canvasRef])
  return (
    <div
      ref={containerRef}
      className={`ambient-panel relative overflow-hidden ${className || ''}`}
      style={{ ...style, position: 'relative' }}
    >
      {visible && (
        <canvas
          ref={canvasRef}
          className="ambient-particles-canvas"
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            pointerEvents: 'none',
            zIndex: 0,
            opacity: 0.6
          }}
          aria-hidden="true"
        />
      )}
      <div className="ambient-panel-content relative" style={{ zIndex: 1 }}>
        {children}
      </div>
    </div>
  )
}
export { AmbientParticlePanel }
export default AmbientParticlePanel
```
SettingsToggle.jsx
```javascript
import React, { useCallback, useEffect, useState } from 'react'
function getDeviceProfile() {
  if (typeof navigator === 'undefined') return { isMobile: false, isLowPower: false }
  const ua = navigator.userAgent || ''
  const isMobile = /Android|iPhone|iPad|iPod|webOS|BlackBerry|IEMobile|Opera Mini/i.test(ua)
  const isLowPower = navigator.hardwareConcurrency <= 4 || 
    ('deviceMemory' in navigator && navigator.deviceMemory <= 4)
  return { isMobile, isLowPower }
}
function AmbientParticleSettings({ enabled, onToggle }) {
  const [localEnabled, setLocalEnabled] = useState(enabled)
  const [showSettings, setShowSettings] = useState(false)
  const profile = getDeviceProfile()
  useEffect(() => {
    setLocalEnabled(enabled)
  }, [enabled])
  const handleToggle = useCallback(() => {
    const next = !localEnabled
    setLocalEnabled(next)
    if (onToggle) onToggle(next)
  }, [localEnabled, onToggle])
  if (profile.isMobile) {
    return null
  }
  return (
    <div className="ambient-settings">
      <button
        className="ambient-settings-toggle"
        onClick={() => setShowSettings(s => !s)}
        aria-label="Ambient particles settings"
        title="Toggle ambient particles"
        type="button"
      >
        p
      </button>
      {showSettings && (
        <div className="ambient-settings-dropdown">
          <label className="ambient-settings-label">
            <input
              type="checkbox"
              checked={localEnabled}
              onChange={handleToggle}
              disabled={profile.isLowPower}
            />
            <span>Ambient particles</span>
          </label>
          {profile.isLowPower && (
            <span className="ambient-settings-hint">Disabled on low-power devices</span>
          )}
        </div>
      )}
    </div>
  )
}
export { AmbientParticleSettings }
export default AmbientParticleSettings
```
index.js
```javascript
export { AmbientParticleSystem, Particle, SPAWN_RATE, PARTICLE_LIMIT, TEMP_RAMP } from './AmbientParticleSystem'
export { useAmbientParticles } from './useAmbientParticles'
export { AmbientParticlePanel } from './AmbientParticlePanel'
export { AmbientParticleSettings } from './SettingsToggle'
```
Summary of what this delivers:
Particle types: ember (rise slow, glow), spark (fast, short-lived, burst-capable), haze (large blurred blobs, barely visible)
Data reactivity:
  forgeActivitySource callback drives spawn rate (idle 0.3 up to active 2.0)
  gpuTempSource callback drives color ramp (0-0.3 cool blue, 0.3-0.6 warm amber, 0.6-1.0 hot red)
  promoteSource triggers burst of 30 sparks with outward velocity
Performance:
  hard cap at 200 particles, drops to 100 on mobile/low-power
  requestAnimationFrame with delta-time dampening
  auto-disabled on battery < 20% via getBattery API
  off by default on mobile
  togglable via settings panel toggle button