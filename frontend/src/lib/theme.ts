/**
 * SmartCropX Glassmorphism Design System
 * Comprehensive design tokens for premium, modern agricultural AI interface
 */

export const glassTheme = {
  // ================================================================
  // COLOR PALETTE
  // ================================================================
  colors: {
    // Primary backgrounds - deep emerald/slate foundation
    bg: {
      primary: 'linear-gradient(135deg, #0f172a 0%, #064e3b 100%)', // slate-950 to emerald-900
      secondary: 'linear-gradient(135deg, #1e293b 0%, #0d7377 100%)', // slate-800 to teal-900
      accent: 'linear-gradient(135deg, #0d7377 0%, #00b8a9 100%)', // teal-900 to teal-500
    },

    // Glass overlays - semantic transparency levels
    glass: {
      sm: 'rgba(255, 255, 255, 0.05)',      // very subtle
      md: 'rgba(255, 255, 255, 0.10)',      // default glass
      lg: 'rgba(255, 255, 255, 0.15)',      // elevated glass
      xl: 'rgba(255, 255, 255, 0.20)',      // strong glass
      hover: 'rgba(255, 255, 255, 0.12)',   // hover state
      focus: 'rgba(255, 255, 255, 0.18)',   // focus state
    },

    // Borders - glass edges with varying strength
    border: {
      subtle: 'rgba(255, 255, 255, 0.10)',
      default: 'rgba(255, 255, 255, 0.15)',
      strong: 'rgba(255, 255, 255, 0.25)',
      success: 'rgba(34, 197, 94, 0.30)',   // green-500/30
      warning: 'rgba(251, 146, 60, 0.30)',  // orange-500/30
      error: 'rgba(239, 68, 68, 0.30)',     // red-500/30
      info: 'rgba(34, 184, 207, 0.30)',     // cyan-500/30
    },

    // Text hierarchy - white with semantic opacity
    text: {
      primary: '#ffffff',             // white
      secondary: 'rgba(255, 255, 255, 0.75)',
      tertiary: 'rgba(255, 255, 255, 0.60)',
      muted: 'rgba(255, 255, 255, 0.50)',
      disabled: 'rgba(255, 255, 255, 0.40)',
    },

    // Semantic colors - accent palette
    semantic: {
      success: '#22c55e',    // emerald-500
      warning: '#fb923c',    // orange-500
      error: '#ef4444',      // red-500
      info: '#22b8d4',       // cyan-500
    },

    // Accents - emerald, teal, cyan
    accent: {
      primary: '#10b981',    // emerald-500
      secondary: '#14b8a6',  // teal-500
      tertiary: '#06b6d4',   // cyan-500
    },
  },

  // ================================================================
  // SHADOWS & GLOWS
  // ================================================================
  shadows: {
    // Glass card shadows - soft and ambient
    glass: {
      sm: '0 8px 32px rgba(0, 0, 0, 0.1)',
      md: '0 8px 32px rgba(0, 0, 0, 0.15)',
      lg: '0 20px 48px rgba(0, 0, 0, 0.25)',
      xl: '0 30px 60px rgba(0, 0, 0, 0.35)',
    },

    // Glow effects for hover/focus
    glow: {
      success: '0 0 24px rgba(34, 197, 94, 0.25)',
      warning: '0 0 24px rgba(251, 146, 60, 0.25)',
      error: '0 0 24px rgba(239, 68, 68, 0.25)',
      info: '0 0 24px rgba(34, 184, 207, 0.25)',
    },
  },

  // ================================================================
  // BLUR EFFECTS
  // ================================================================
  blur: {
    sm: 'blur(8px)',
    md: 'blur(12px)',
    lg: 'blur(16px)',
    xl: 'blur(24px)',
  },

  // ================================================================
  // SPACING SCALE
  // ================================================================
  spacing: {
    container: 'max-w-7xl mx-auto px-4 md:px-6 lg:px-8',
    section: 'py-12 md:py-16 lg:py-20',
    gap: {
      xs: 'gap-2',
      sm: 'gap-3',
      md: 'gap-4',
      lg: 'gap-6',
      xl: 'gap-8',
    },
  },

  // ================================================================
  // BORDER RADIUS
  // ================================================================
  radius: {
    icon: '0.75rem',      // 12px - icon buttons
    button: '0.875rem',   // 14px - buttons
    input: '1rem',        // 16px - inputs
    card: '1.5rem',       // 24px - cards
    modal: '2rem',        // 32px - modals
    hero: '2.5rem',       // 40px - large sections
  },

  // ================================================================
  // BACKDROP BLUR LEVELS
  // ================================================================
  backdrop: {
    none: 'backdrop-blur-0',
    sm: 'backdrop-blur-sm',
    md: 'backdrop-blur-md',
    lg: 'backdrop-blur-lg',
    xl: 'backdrop-blur-xl',
  },

  // ================================================================
  // TRANSITIONS
  // ================================================================
  transitions: {
    fast: 'transition-all duration-200 ease-in-out',
    base: 'transition-all duration-300 ease-in-out',
    slow: 'transition-all duration-500 ease-in-out',
  },
};

/**
 * CSS class utilities derived from theme
 * Use these in className for quick glass component styling
 */
export const glassClasses = {
  // Page containers
  pageWrapper: 'min-h-screen w-full bg-gradient-to-br from-slate-950 via-emerald-950 to-teal-950',
  pageContainer: 'max-w-7xl mx-auto px-4 md:px-6 lg:px-8',
  section: 'py-12 md:py-16 lg:py-20',

  // Glass cards
  glassCard: 'bg-white/10 backdrop-blur-md border border-white/15 rounded-2xl shadow-lg hover:bg-white/12 hover:border-white/20 transition-all duration-300',
  glassCardElevated: 'bg-white/15 backdrop-blur-lg border border-white/25 rounded-3xl shadow-xl hover:bg-white/18 hover:border-white/30 transition-all duration-300',
  glassCardCompact: 'bg-white/10 backdrop-blur-md border border-white/15 rounded-xl shadow-md hover:bg-white/12 transition-all duration-300',

  // Glass buttons
  buttonPrimary: 'px-6 py-2.5 rounded-xl bg-emerald-500/80 hover:bg-emerald-500 text-white font-semibold border border-emerald-400/30 backdrop-blur-sm shadow-lg hover:shadow-emerald-500/25 transition-all duration-300 hover:scale-105',
  buttonSecondary: 'px-6 py-2.5 rounded-xl bg-white/10 hover:bg-white/15 text-white font-semibold border border-white/20 hover:border-white/30 backdrop-blur-md shadow-md transition-all duration-300 hover:scale-105',
  buttonGhost: 'px-4 py-2 rounded-lg text-white/80 hover:text-white hover:bg-white/10 border border-white/10 hover:border-white/20 transition-all duration-300',

  // Glass inputs
  input: 'w-full px-4 py-3 rounded-xl bg-white/10 backdrop-blur-md border border-white/15 text-white placeholder-white/40 focus:border-white/30 focus:bg-white/12 focus:outline-none transition-all duration-300 shadow-md',

  // Text utilities
  textPrimary: 'text-white font-semibold',
  textSecondary: 'text-white/75',
  textMuted: 'text-white/60',

  // Badge
  badge: 'inline-block px-3 py-1 rounded-full bg-white/10 backdrop-blur-md text-xs font-semibold text-white/90 border border-white/20',
  badgeSuccess: 'inline-block px-3 py-1 rounded-full bg-emerald-500/20 text-xs font-semibold text-emerald-200 border border-emerald-400/30',
  badgeWarning: 'inline-block px-3 py-1 rounded-full bg-orange-500/20 text-xs font-semibold text-orange-200 border border-orange-400/30',
  badgeError: 'inline-block px-3 py-1 rounded-full bg-red-500/20 text-xs font-semibold text-red-200 border border-red-400/30',
};
