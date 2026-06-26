┊ review diff
[38;2;218;165;32ma/StydeAgents\blueprints\jetpack-compose-expert\BLUEPRINT.md → b/StydeAgents\blueprints\jetpack-compose-expert\BLUEPRINT.md[0m
[38;2;139;134;130m@@ -13,3 +13,70 @@[0m
[38;2;184;134;11m - Room: use Room database with Flow[0m
[38;2;184;134;11m - Nav: implement type-safe navigation[0m
[38;2;184;134;11m - DI: use Hilt for dependency injection[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Testing[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Unit Tests[0m
[38;2;255;255;255;48;2;19;87;20m+- Use JUnit 5 for all business logic, ViewModel state assertions, and repository tests[0m
[38;2;255;255;255;48;2;19;87;20m+- Use MockK for dependency mocking — prefer relaxed mocks for ViewModel dependencies, verify exact call counts on critical paths[0m
[38;2;255;255;255;48;2;19;87;20m+- Test each ViewModel's state machine transitions (loading → success / loading → error) with explicit state assertions[0m
[38;2;255;255;255;48;2;19;87;20m+- Structure test files per class: `MyViewModelTest`, `MyRepositoryTest`[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Compose UI Tests[0m
[38;2;255;255;255;48;2;19;87;20m+- Use Compose Test Rule (`createComposeRule`) for all composable screen tests[0m
[38;2;255;255;255;48;2;19;87;20m+- Assert via Compose semantics: `onNodeWithTag`, `onNodeWithText`, `assertIsDisplayed`, `performClick`[0m
[38;2;255;255;255;48;2;19;87;20m+- Assign unique `testTag` modifiers to interactive elements (buttons, text fields, list items)[0m
[38;2;255;255;255;48;2;19;87;20m+- Test navigation flows end-to-end with `NavHostController` in `ComposeTestRule`[0m
[38;2;255;255;255;48;2;19;87;20m+- Avoid `Thread.sleep()` — use `waitForIdle()` and `SemanticsMatcher.expectValue(...)` for async state[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Coroutine Test Dispatchers[0m
[38;2;255;255;255;48;2;19;87;20m+- Use `UnconfinedTestDispatcher` or `StandardTestDispatcher` from `kotlinx-coroutines-test`[0m
[38;2;255;255;255;48;2;19;87;20m+- Inject dispatchers via ViewModel constructor parameters typed as `CoroutineDispatcher` (default: `Dispatchers.Main`)[0m
[38;2;255;255;255;48;2;19;87;20m+- Call `runTest` for every coroutine-dependent test; use `advanceUntilIdle()` or `advanceTimeBy()` for timing-dependent flows[0m
[38;2;255;255;255;48;2;19;87;20m+- Reset `Dispatchers.Main` in `@Before`/`@After` using `Dispatchers.setMain(testDispatcher)` / `Dispatchers.resetMain()`[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Compose Conventions[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Previews[0m
[38;2;255;255;255;48;2;19;87;20m+- Add a `@Preview(showBackground = true)` composable for every screen and every reusable component[0m
[38;2;255;255;255;48;2;19;87;20m+- Use `@Preview(uiMode = Configuration.UI_MODE_NIGHT_YES)` variant for dark mode coverage[0m
[38;2;255;255;255;48;2;19;87;20m+- Wrap previews in a theme wrapper composable that applies `MaterialTheme` so they render with correct colors and typography[0m
[38;2;255;255;255;48;2;19;87;20m+- Name preview functions descriptively: `ScreenLoadingPreview`, `ScreenContentPreview`, `ScreenErrorPreview`[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### State Hoisting[0m
[38;2;255;255;255;48;2;19;87;20m+- Hoist all mutable UI state to the ViewModel — composables should have zero mutable state fields[0m
[38;2;255;255;255;48;2;19;87;20m+- ViewModel exposes `StateFlow<UiState>` (sealed interface with `Loading`, `Success(data)`, `Error(message)` variants)[0m
[38;2;255;255;255;48;2;19;87;20m+- Composables collect state via `val state by viewModel.uiState.collectAsStateWithLifecycle()`[0m
[38;2;255;255;255;48;2;19;87;20m+- One-shot events (navigation, snackbar) use `SharedFlow<UiEvent>` collected with `LaunchedEffect`[0m
[38;2;255;255;255;48;2;19;87;20m+- ViewModel actions are function calls, never state mutations from the composable layer[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Compose Compiler Version[0m
[38;2;255;255;255;48;2;19;87;20m+- Compose Compiler version must exactly match the Kotlin version per the official compatibility table[0m
[38;2;255;255;255;48;2;19;87;20m+- In `build.gradle.kts` (module): `composeCompiler { kotlinCompilerExtensionVersion = "1.5.8" }`[0m
[38;2;255;255;255;48;2;19;87;20m+- Verify: `kotlin("plugin.compose") version "$kotlinVersion"` in the project-level plugin block[0m
[38;2;255;255;255;48;2;19;87;20m+- When upgrading Kotlin, update the Compose compiler extension version in lockstep[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Coroutine & Flow Scoping[0m
[38;2;255;255;255;48;2;19;87;20m+- `viewModelScope` for all ViewModel-initiated flows — automatically cancelled on ViewModel clear[0m
[38;2;255;255;255;48;2;19;87;20m+- `lifecycleScope` (with `repeatOnLifecycle(Lifecycle.State.STARTED)`) for composable-level effects that must respect lifecycle[0m
[38;2;255;255;255;48;2;19;87;20m+- `LaunchedEffect` for one-shot coroutine work tied to a composable's composition lifecycle[0m
[38;2;255;255;255;48;2;19;87;20m+- `rememberCoroutineScope()` only for user-triggered actions in composables that need a scope independent of lifecycle (rare — prefer ViewModel delegation)[0m
[38;2;255;255;255;48;2;19;87;20m+- Inject `Dispatchers.IO`, `Dispatchers.Default` via constructor parameters for testability, never hard-code in ViewModels[0m
[38;2;255;255;255;48;2;19;87;20m+- Flow collections on UI: always `stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), initialValue)` for cold-to-hot conversion[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Probe/Response Lifecycle[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+### Fallback Escalation[0m
[38;2;255;255;255;48;2;19;87;20m+When a probe response is insufficient (missing fields, vague descriptions, contradictory data):[0m
[38;2;255;255;255;48;2;19;87;20m+1. Request specific missing fields — name each field and its expected format[0m
[38;2;255;255;255;48;2;19;87;20m+2. Ask for a worked example — prompt the user/source to provide a concrete instance[0m
[38;2;255;255;255;48;2;19;87;20m+3. Fall back to a default structure — apply a sensible default (empty state, placeholder values, estimated data) clearly marked as inferred[0m
[38;2;255;255;255;48;2;19;87;20m+4. Log the fallback decision in the response metadata so the caller can audit completeness[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+## Production Checklist[0m
[38;2;255;255;255;48;2;19;87;20m+Before finishing any feature or screen, verify:[0m
[38;2;255;255;255;48;2;19;87;20m+1. Tests written — unit tests for ViewModel logic, UI tests for critical flows[0m
[38;2;255;255;255;48;2;19;87;20m+2. Compose previews present — light + dark mode for every screen[0m
[38;2;255;255;255;48;2;19;87;20m+3. State hoisted to ViewModel — no mutable state in composables[0m
[38;2;255;255;255;48;2;19;87;20m+4. Coroutine scope matches lifecycle — viewModelScope / lifecycleScope / LaunchedEffect used correctly[0m
[38;2;255;255;255;48;2;19;87;20m+5. Compose compiler version aligns with Kotlin version[0m
  ┊ review diff
[38;2;218;165;32ma/StydeAgents\blueprints\jetpack-compose-expert\persona.md → b/StydeAgents\blueprints\jetpack-compose-expert\persona.md[0m
[38;2;139;134;130m@@ -1,8 +1,16 @@[0m
[38;2;184;134;11m You are Android developer. Expert in Kotlin, Jetpack Compose, Material 3, and Android architecture..[0m
[38;2;184;134;11m [0m
[38;2;184;134;11m Rules:[0m
[38;2;255;255;255;48;2;119;20;20m-- Compose: build UIs with Jetpack Compose[0m
[38;2;255;255;255;48;2;119;20;20m-- M3: implement Material Design 3 components[0m
[38;2;255;255;255;48;2;119;20;20m-- Room: use Room database with Flow[0m
[38;2;255;255;255;48;2;119;20;20m-- Nav: implement type-safe navigation[0m
[38;2;255;255;255;48;2;119;20;20m-- DI: use Hilt for dependency injection[0m
[38;2;255;255;255;48;2;19;87;20m+  Compose: build UIs with Jetpack Compose[0m
[38;2;255;255;255;48;2;19;87;20m+  M3: implement Material Design 3 components[0m
[38;2;255;255;255;48;2;19;87;20m+  Room: use Room database with Flow[0m
[38;2;255;255;255;48;2;19;87;20m+  Nav: implement type-safe navigation[0m
[38;2;255;255;255;48;2;19;87;20m+  DI: use Hilt for dependency injection[0m
[38;2;255;255;255;48;2;19;87;20m+[0m
[38;2;255;255;255;48;2;19;87;20m+Checklist:[0m
[38;2;255;255;255;48;2;19;87;20m+  Before finishing, verify:[0m
[38;2;255;255;255;48;2;19;87;20m+  1. tests written[0m
[38;2;255;255;255;48;2;19;87;20m+  2. Compose previews present[0m
[38;2;255;255;255;48;2;19;87;20m+  3. state hoisted to ViewModel[0m
[38;2;255;255;255;48;2;19;87;20m+  4. coroutine scope matches lifecycle[0m
[38;2;255;255;255;48;2;19;87;20m+  5. Compose compiler version aligns with Kotlin[0m
Bada fungerar. Båda filerna uppdaterade:
BLUEPRINT.md:
- Testing - JUnit 5, MockK, Compose Test Rule, coroutine test dispatchers med UnconfinedTestDispatcher/StandardTestDispatcher, runTest/advanceUntilIdle
- Compose Conventions - Previews med light + dark mode, state hoisting via ViewModel + StateFlow + collectAsStateWithLifecycle, Compose compiler version matching Kotlin
- Coroutine & Flow Scoping - viewModelScope, lifecycleScope + repeatOnLifecycle, LaunchedEffect, Dispatchers-injektion, stateIn med WhileSubscribed(5000)
- Fallback Escalation - 4-steg: begär specifika fält, be om exempel, fallback till default-struktur, logga beslutet
- Production Checklist - 5-punkterslista som sammanfattar allt ovan
persona.md:
- Checklist-sektion tillagd med samma 5 punkter
D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\jetpack-compose-expert\BLUEPRINT.md (82 rader)
D:\styde\_alpedal\styde-forge\StydeAgents\blueprints\jetpack-compose-expert\persona.md (16 rader)