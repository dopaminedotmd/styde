domain: app-dev
blueprint: Capacitor Hybrid Builder
version: 1
status: validated
skills:
  plugin:
    status: ready
    approach: capacitor generate plugin scaffold, define web-native interfaces with @capacitor/plugin-migration, expose via registerPlugin()
  native:
    camera: Camera.getPhoto() with permission checks + fallback to Picker
    geolocation: Geolocation.getCurrentPosition() + watchPosition() with accuracy config
    filesystem: Filesystem.readFile/writeFile with base64 encoding, share via Share plugin
  bridge:
    optimization: capacitor-bridge-spi for low-latency calls, avoid serialization of large blobs, use content URIs instead of base64 for images
    pattern: one-directional data flow, keep JS-to-native calls under 100ms, batch events via addListener
  deploy:
    ios: npx cap sync ios && npx cap open ios, code signing via xcconfig env vars
    android: npx cap sync android && npx cap open android, keystore config in build.gradle
    parallel: npm run build && npx cap sync, then deploy to both simultaneously via fastlane
  live:
    development: npx cap serve with --external flag for device testing
    reload: use @capacitor/cli development server with SSL passthrough, watch for web asset changes via Vite middleware
caveats:
  - capacitor v6 drops support for android api 21, target api 24+
  - ios requires info.plist entries for camera/photo/gps usage descriptions
  - live reload needs same network segment or vpn tunnel
  - custom plugins must implement both ios (swift/cocoapods) and android (java/kotlin) layers
  - splash screen and icon config moved to capacitor.config.ts in v5+
scaffold:
  npm init @capacitor/app
  npm install @capacitor/core @capacitor/cli @capacitor/android @capacitor/ios
  npx cap init
  npx cap add android
  npx cap add ios