// CarbonLens Minimal Noir Design Tokens
// Source of truth: total.html

export const colors = {
  // Architectural Canvas & Surfaces
  canvasBase: '#0B0B0B',
  surfacePrimary: '#141414',
  surfaceSecondary: '#1E1E1E',
  surfaceTranslucent: {
    low: 'rgba(255, 255, 255, 0.03)',
    high: 'rgba(255, 255, 255,农村 0.06)',
  },
  
  // Line Work & Highlights
  hairlineBorder: 'rgba(255, 255, 255, 0.08)',
  activeBorder: 'rgba(255, 255, 255, 0.22)',
  specularEdge: 'rgba(255, 255, 255, 0.12)',
  
  // Typography & Content
  textPrimary: '#FFFFFF',
  textSecondary: '#AFAFAF',
  textTertiary: '#5F5F5F',
  textMuted: '#5F5F5F',
  
  // From total.html design system
  surface: '#131313',
  surfaceDim: '#131313',
  surfaceBright: '#3a3939',
  surfaceContainerLowest: '#0e0e0e',
  surfaceContainerLow: '#1c1b1b',
  surfaceContainer: '#201f1f',
  surfaceContainerHigh: '#2a2a2a',
  surfaceContainerHighest: '#353534',
  onSurface: '#e5e2e1',
  onSurfaceVariant: '#c4c7c8',
  outline: '#8e9192',
  outlineVariant: '#444748',
  primary: '#ffffff',
  onPrimary: '#2f3131',
  primaryContainer: '#e2e2e2',
  onPrimaryContainer: '#636565',
  secondary: '#c7c6c6',
  onSecondary: '#2f3131',
  secondaryContainer: '#484949',
  onSecondaryContainer: '#b8b8b8',
  tertiary: '#ffffff',
  onTertiary: '#303031',
  tertiaryContainer: '#e4e2e2',
  onTertiaryContainer: '#646464',
  error: '#ffb4ab',
  onError: '#690005',
  errorContainer: '#93000a',
  onErrorContainer: '#ffdad6',
  background: '#131313',
  onBackground: '#e5e2e1',
  surfaceVariant: '#353534',
}

export const typography = {
  // Font families
  fontFamily: {
    sans: 'Geist, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    mono: 'ui-monospace, Consolas, monospace',
  },
  
  // Font sizes and line heights from total.html
  displayHero: {
    fontSize: '80px',
    lineHeight: '84px',
    fontWeight: '600',
    letterSpacing: '-0.04em',
  },
  displayHeroMobile: {
    fontSize: '48px',
    lineHeight: '52px',
    fontWeight: '600',
    letterSpacing: '-0.03em',
  },
  headlineXl: {
    fontSize: '44px',
    lineHeight: '48px',
    fontWeight: '600',
    letterSpacing: '-0.03em',
  },
  headlineXlMobile: {
    fontSize: '32px',
    lineHeight: '36px',
    fontWeight: '600',
    letterSpacing: '-0.02em',
  },
  headlineLg: {
    fontSize: '28px',
    lineHeight: '34px',
    fontWeight: '500',
    letterSpacing: '-0.02em',
  },
  headlineMd: {
    fontSize: '20px',
    lineHeight: '26px',
    fontWeight: '500',
    letterSpacing: '-0.015em',
  },
  bodyLg: {
    fontSize: '16px',
    lineHeight: '24px',
    fontWeight: '400',
    letterSpacing: '-0.01em',
  },
  bodyMd: {
    fontSize: '14px',
    lineHeight: '20px',
    fontWeight: '400',
    letterSpacing: '-0.005em',
  },
  bodySm: {
    fontSize: '12px',
    lineHeight: '16px',
    fontWeight: '400',
    letterSpacing: '0em',
  },
  eyebrowTag: {
    fontSize: '11px',
    lineHeight: '14px',
    fontWeight: '600',
    letterSpacing: '0.12em',
  },
  labelMd: {
    fontSize: '13px',
    lineHeight: '16px',
    fontWeight: '500',
    letterSpacing: '-0.005em',
  },
  labelSm: {
    fontSize: '11px',
    lineHeight: '14px',
    fontWeight: '500',
    letterSpacing: '0.02em',
  },
  metricLarge: {
    fontSize: '56px',
    lineHeight: '60px',
    fontWeight: '600',
    letterSpacing: '-0.04em',
  },
}

export const borderRadius = {
  sm: '0.25rem',
  DEFAULT: '0.5rem',
  md: '0.75rem',
  lg: '1rem',
  xl: '1.5rem',
  full: '9999px',
}

export const spacing = {
  gutter: '1.5rem',
  gutterSm: '1rem',
  margin: '2.5rem',
  marginSm: '1.25rem',
  spaceXs: '0.25rem',
  spaceSm: '0.5rem',
  spaceMd: '1rem',
  spaceLg: '1.5rem',
  spaceXl: '2.5rem',
}

export const breakpoints = {
  mobile: '768px',
  tablet: '1200px',
  desktop: '1440px',
}