design-tokens.yaml:
colors:
  brand:
    primary: { light: '#6366F1', dark: '#818CF8' }
    secondary: { light: '#8B5CF6', dark: '#A78BFA' }
    accent: { light: '#F59E0B', dark: '#FBBF24' }
  neutral:
    50: { light: '#FAFAFA', dark: '#0A0A0A' }
    100: { light: '#F5F5F5', dark: '#141414' }
    200: { light: '#E5E5E5', dark: '#262626' }
    300: { light: '#D4D4D4', dark: '#404040' }
    400: { light: '#A3A3A3', dark: '#737373' }
    500: { light: '#737373', dark: '#A3A3A3' }
    600: { light: '#525252', dark: '#D4D4D4' }
    700: { light: '#404040', dark: '#E5E5E5' }
    800: { light: '#262626', dark: '#F5F5F5' }
    900: { light: '#171717', dark: '#FAFAFA' }
  semantic:
    success: { light: '#22C55E', dark: '#4ADE80' }
    warning: { light: '#F59E0B', dark: '#FBBF24' }
    error: { light: '#EF4444', dark: '#F87171' }
    info: { light: '#3B82F6', dark: '#60A5FA' }
  surface:
    page: { light: '#FFFFFF', dark: '#0A0A0A' }
    card: { light: '#FAFAFA', dark: '#141414' }
    overlay: { light: 'rgba(0,0,0,0.4)', dark: 'rgba(0,0,0,0.6)' }
  text:
    primary: { light: '#171717', dark: '#FAFAFA' }
    secondary: { light: '#737373', dark: '#A3A3A3' }
    disabled: { light: '#A3A3A3', dark: '#525252' }
    inverse: { light: '#FFFFFF', dark: '#171717' }
spacing:
  scale: [0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96]
  semantic:
    xs: 4
    sm: 8
    md: 16
    lg: 24
    xl: 32
    xxl: 48
    section: 80
  layout:
    pagePadding: { mobile: 16, tablet: 24, desktop: 32 }
    gridGap: { mobile: 16, tablet: 24, desktop: 32 }
    maxWidth: 1200
typography:
  fontFamily:
    sans: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    mono: "'JetBrains Mono', 'Fira Code', monospace"
  fontSize:
    xs: 12
    sm: 14
    base: 16
    lg: 18
    xl: 20
    h4: 24
    h3: 30
    h2: 36
    h1: 48
    display: 64
  fontWeight:
    normal: 400
    medium: 500
    semibold: 600
    bold: 700
  lineHeight:
    tight: 1.2
    base: 1.5
    relaxed: 1.75
  textStyles:
    display:
      fontFamily: sans
      fontSize: display
      fontWeight: bold
      lineHeight: tight
      letterSpacing: -0.025em
    h1:
      fontFamily: sans
      fontSize: h1
      fontWeight: bold
      lineHeight: tight
    h2:
      fontFamily: sans
      fontSize: h2
      fontWeight: semibold
      lineHeight: tight
    h3:
      fontFamily: sans
      fontSize: h3
      fontWeight: semibold
      lineHeight: tight
    h4:
      fontFamily: sans
      fontSize: h4
      fontWeight: semibold
      lineHeight: base
    body:
      fontFamily: sans
      fontSize: base
      fontWeight: normal
      lineHeight: base
    bodySmall:
      fontFamily: sans
      fontSize: sm
      fontWeight: normal
      lineHeight: base
    caption:
      fontFamily: sans
      fontSize: xs
      fontWeight: normal
      lineHeight: base
    code:
      fontFamily: mono
      fontSize: sm
      fontWeight: normal
      lineHeight: base
shadows:
  sm: { light: '0 1px 2px rgba(0,0,0,0.05)', dark: '0 1px 2px rgba(0,0,0,0.3)' }
  md: { light: '0 4px 6px rgba(0,0,0,0.07)', dark: '0 4px 6px rgba(0,0,0,0.4)' }
  lg: { light: '0 10px 15px rgba(0,0,0,0.1)', dark: '0 10px 15px rgba(0,0,0,0.5)' }
  xl: { light: '0 20px 25px rgba(0,0,0,0.15)', dark: '0 20px 25px rgba(0,0,0,0.6)' }
  focus: { light: '0 0 0 3px rgba(99,102,241,0.25)', dark: '0 0 0 3px rgba(129,140,248,0.3)' }
borderRadius:
  none: 0
  sm: 4
  md: 8
  lg: 12
  xl: 16
  full: 9999
breakpoints:
  mobile: 0
  tablet: 640
  desktop: 1024
  wide: 1280
transitions:
  fast: '150ms ease'
  base: '250ms ease'
  slow: '400ms ease'
components/Button.yaml:
name: Button
description: Primary action trigger. Supports hierarchy, size, and icon variants.
props:
  variant:
    type: enum
    values: [primary, secondary, tertiary, ghost, danger]
    default: primary
  size:
    type: enum
    values: [sm, md, lg]
    default: md
  fullWidth:
    type: boolean
    default: false
  disabled:
    type: boolean
    default: false
  loading:
    type: boolean
    default: false
  icon:
    type: icon-name
    default: null
  iconPosition:
    type: enum
    values: [left, right]
    default: left
  children:
    type: node
    required: false
rules:
  - primary variant uses brand.primary background, white text
  - secondary variant uses transparent background with border
  - tertiary variant has no border or background, only text
  - ghost variant is transparent until hovered
  - danger variant uses semantic.error background
  - loading state replaces children with spinner icon
  - disabled state reduces opacity to 0.5, removes pointer events
  - icon + text spacing is 8px
  - md size padding: 12px 20px, font-size: 14px
  - sm size padding: 8px 16px, font-size: 12px
  - lg size padding: 16px 28px, font-size: 16px
components/Card.yaml:
name: Card
description: Container for grouped content. Supports padding variants and hover effects.
props:
  padding:
    type: enum
    values: [none, sm, md, lg]
    default: md
  variant:
    type: enum
    values: [elevated, outlined, flat]
    default: elevated
  hoverable:
    type: boolean
    default: false
  onClick:
    type: function
    default: null
rules:
  - elevated variant uses shadow.md
  - outlined variant uses border 1px solid neutral.200
  - flat variant has no shadow or border
  - hoverable adds transform translateY(-2px) and shadow transition
  - Card body padding: padding prop maps to spacing scale
  - Card.Header and Card.Footer are optional subcomponents
  - background uses surface.card token
  - border-radius: borderRadius.md
components/Input.yaml:
name: Input
description: Text entry field with label, helper text, and validation states.
props:
  label:
    type: string
    default: null
  placeholder:
    type: string
    default: null
  type:
    type: enum
    values: [text, email, password, number, search, tel, url]
    default: text
  size:
    type: enum
    values: [sm, md, lg]
    default: md
  disabled:
    type: boolean
    default: false
  readOnly:
    type: boolean
    default: false
  error:
    type: string
    default: null
  helperText:
    type: string
    default: null
  required:
    type: boolean
    default: false
  prefix:
    type: node
    default: null
  suffix:
    type: node
    default: null
states:
  default:
    border: neutral.300
    background: surface.card
  focus:
    border: brand.primary
    shadow: shadows.focus
  error:
    border: semantic.error
    shadow: '0 0 0 3px rgba(239,68,68,0.2)'
  disabled:
    background: neutral.100
    opacity: 0.6
components/Modal.yaml:
name: Modal
description: Overlay dialog for focused interactions. Traps focus, handles escape key.
props:
  open:
    type: boolean
    default: false
  onClose:
    type: function
    required: true
  title:
    type: string
    default: null
  size:
    type: enum
    values: [sm, md, lg, xl, fullscreen]
    default: md
  closeOnOverlay:
    type: boolean
    default: true
  closeOnEscape:
    type: boolean
    default: true
  preventScroll:
    type: boolean
    default: true
slots:
  header: title area, close button
  body: primary content
  footer: action buttons
rules:
  - overlay uses surface.overlay color
  - content background uses surface.page
  - border-radius: borderRadius.lg
  - z-index: 50
  - animation: fade in 250ms
  - focus trap within modal content
  - aria-modal: true, role: dialog
components/Select.yaml:
name: Select
description: Dropdown selection from predefined options. Supports search and groups.
props:
  options:
    type: array
    items: { label: string, value: string, disabled: boolean }
    required: true
  placeholder:
    type: string
    default: 'Select...'
  searchable:
    type: boolean
    default: false
  clearable:
    type: boolean
    default: false
  size:
    type: enum
    values: [sm, md, lg]
    default: md
  error:
    type: string
    default: null
  multi:
    type: boolean
    default: false
  maxSelected:
    type: number
    default: null
rules:
  - dropdown panel uses shadow.lg, z-index: 40
  - selected option shown in input field
  - searchable adds input filter at top of dropdown
  - multi mode shows tags in input area
  - option hover uses brand.primary at 10% opacity
  - selected option uses brand.primary at 20% opacity
components/Tabs.yaml:
name: Tabs
description: Navigation between related content panels. Supports line and pill styles.
props:
  tabs:
    type: array
    items: { label: string, value: string, disabled: boolean, icon: icon-name }
    required: true
  active:
    type: string
    required: true
  onChange:
    type: function
    required: true
  variant:
    type: enum
    values: [line, pill, underline]
    default: line
  size:
    type: enum
    values: [sm, md, lg]
    default: md
rules:
  - line variant uses bottom border on active tab
  - pill variant uses background color on active tab
  - underline variant uses thick bottom border on active tab
  - disabled tabs reduce opacity to 0.4
  - tab padding: 12px 16px
  - active indicator color: brand.primary
  - horizontal scrolling on mobile with overflow-x: auto
components/Table.yaml:
name: Table
description: Structured data display with sorting, filtering, and row selection.
props:
  columns:
    type: array
    items: { key: string, label: string, sortable: boolean, width: string, align: string }
    required: true
  data:
    type: array
    required: true
  sortable:
    type: boolean
    default: false
  selectable:
    type: boolean
    default: false
  stickyHeader:
    type: boolean
    default: true
  striped:
    type: boolean
    default: false
  compact:
    type: boolean
    default: false
rules:
  - header uses neutral.100 background
  - cell padding: compact 8px, default 12px 16px
  - sorted column shows arrow indicator
  - hover row highlights at neutral.50
  - stripe uses alternating neutral.50 background
  - border: 1px solid neutral.200
  - text-align: left unless overridden by column align
  - sticky header z-index: 10
components/Tooltip.yaml:
name: Tooltip
description: Contextual information on hover or focus. Shows after delay.
props:
  content:
    type: string
    required: true
  position:
    type: enum
    values: [top, bottom, left, right]
    default: top
  delay:
    type: number
    default: 300
  maxWidth:
    type: number
    default: 240
rules:
  - background: neutral.800
  - text color: neutral.50
  - font-size: 12px
  - padding: 6px 10px
  - border-radius: 4px
  - arrow points away from trigger element
  - z-index: 60
  - show on hover and keyboard focus
  - hide on scroll
components/Toast.yaml:
name: Toast
description: Transient notification. Auto-dismisses. Stackable.
props:
  message:
    type: string
    required: true
  type:
    type: enum
    values: [success, error, warning, info]
    default: info
  duration:
    type: number
    default: 5000
  action:
    type: { label: string, onClick: function }
    default: null
  onDismiss:
    type: function
    default: null
rules:
  - type determines icon and accent color
  - progress bar shows remaining time
  - dismiss button on hover
  - stack top-right by default
  - animation: slide in 300ms, fade out
  - z-index: 70
  - max visible: 5
components/Badge.yaml:
name: Badge
description: Small label for counts, statuses, or categories.
props:
  variant:
    type: enum
    values: [default, success, warning, error, info, brand]
    default: default
  size:
    type: enum
    values: [sm, md]
    default: md
  dot:
    type: boolean
    default: false
  count:
    type: number
    default: null
  maxCount:
    type: number
    default: 99
rules:
  - variant sets background and text color
  - default variant uses neutral.200 bg
  - dot variant shows small circle instead of pill
  - count variant shows number with + for maxCount overflow
  - border-radius: full for pill, 50% for dot
  - padding: sm 2px 6px, md 4px 10px
  - font-size: sm 10px, md 12px
  - font-weight: 600
themes/brand-override.yaml:
themeName: enterprise
tokens:
  brand:
    primary: '#1E40AF'
    secondary: '#7C3AED'
    accent: '#DC2626'
  typography:
    fontFamily:
      sans: "'SF Pro Display', 'Helvetica Neue', Arial, sans-serif"
  borderRadius:
    md: 6
    lg: 8
rules:
  - themeKey: enterprise
  - extends default tokens
  - only override values that differ from base
consistency-rules.yaml:
spacing:
  - no inline margins or padding outside token scale
  - stack spacing uses spacing tokens, never arbitrary values
  - grid column gap must match layout.gridGap
typography:
  - no font-size declarations outside textStyles
  - no font-weight declarations outside fontWeight tokens
  - line-height must use lineHeight tokens
colors:
  - no hardcoded hex values
  - all colors reference design tokens by name
  - semantic colors used for meaning (error, success), not specific hues
components:
  - every interactive element has focus state
  - every interactive element has disabled state
  - hover transitions use transitions.base
  - clickable area minimum 44x44px per WCAG
  - z-index values from predefined scale: dropdown 40, modal 50, tooltip 60, toast 70
  - no duplicate implementations of same component
  - every component has dark mode equivalent
a11y:
  - color contrast ratio min 4.5:1 for text, 3:1 for large text
  - all form inputs have associated labels
  - all images have alt text
  - interactive elements focusable via keyboard
  - aria attributes on dynamic content
  - prefers-reduced-motion respected
audit-protocol.yaml:
checklist:
  color_usage:
    - scan all css for hex values not in tokens
    - verify semantic color usage
    - confirm dark mode overrides exist
  spacing_consistency:
    - verify all margin/padding match token scale
    - check grid alignment
  component_inventory:
    - catalog all UI components
    - check for duplicate patterns
    - verify every pattern has documented component
  a11y_audit:
    - run axe-core on every page
    - check keyboard navigation
    - verify color contrast
  theme_completeness:
    - confirm all tokens have dark variant
    - confirm theme overrides apply correctly
  regression:
    - screenshot comparison per component
    - layout shift detection
    - interaction state verification