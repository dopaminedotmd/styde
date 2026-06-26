Blueprint valid and loaded. Flutter UI Builder agent ready.
Material Design 3: M3 color scheme from seed color, dynamic color on Android 12+, custom `ColorScheme.fromSeed` with tonal palettes. NavigationBar + NavigationDrawer composable. Surface containers with elevation overlays.
State: Riverpod `StateNotifier` + `AsyncValue` for async widgets. `ref.watch` for reactivity. `go_router` for declarative routing with redirect guards.
Widget composition: `Widget` -> `StatelessWidget`/`ConsumerWidget` -> `StatefulWidget`/`ConsumerStatefulWidget`. Builder pattern for conditional layouts. `LayoutBuilder` + `MediaQuery` for responsive breakpoints.
Platform channels: `MethodChannel` with `invokeMethod`. Native handlers in Swift (iOS) / Kotlin (Android). `EventChannel` for streaming sensors.
Tests: `WidgetTester` with `pumpWidget`. `Mockito` for service mocks. Golden file tests for visual regression. Integration tests with `integration_test` package.
Domain: app-dev. Ready for blueprint execution. State the widget, screen, or feature to generate.