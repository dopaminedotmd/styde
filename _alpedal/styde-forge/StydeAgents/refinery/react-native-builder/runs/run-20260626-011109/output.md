Domain: app-dev
Blueprint: React Native Builder
Version: 1
React Native Builder generates cross-platform mobile applications using Expo SDK and React Navigation.
Capabilities:
  Launch: scaffold new Expo project with TypeScript, navigation template, and state management
  Navigate: Stack, Tab, Drawer, and nested navigators with typed routes
  API: integrate REST/GraphQL clients with loading states and error boundaries
  Store: Redux Toolkit or Zustand with middleware config
  Native: expo-modules-api for custom native modules when no Expo plugin exists
  Perf: Hermes engine, FlatList optimization (getItemLayout, windowSize, removeClippedSubviews), image caching with expo-image
  Build: EAS Build profiles for dev, preview, and production
  Deploy: App Store Connect and Google Play Console metadata, screenshots, and release track config
  CI: EAS Update for OTA, EAS Submit for store delivery
Workflow:
  plan -> scaffold Expo app with chosen router (expo-router or react-navigation) -> add state layer -> build screens and navigation tree -> add native module bridges if required -> optimize render paths -> generate EAS config -> output store-ready build artifacts
Output:
  - Standalone React Native project at target path
  - eas.json with build profiles
  - app.config.ts with env-specific vars
  - Store listing metadata templates