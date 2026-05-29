/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Legacy colors
        'smart-green': '#334b35',
        'smart-yellow': '#f7c35f',
        
        // Glass theme palette
        'glass-bg': 'rgba(255, 255, 255, 0.10)',
        'glass-border': 'rgba(255, 255, 255, 0.15)',
        'glass-hover': 'rgba(255, 255, 255, 0.12)',
        'text-secondary': 'rgba(255, 255, 255, 0.75)',
        'text-muted': 'rgba(255, 255, 255, 0.60)',
      },
      backgroundImage: {
        'gradient-glass': 'linear-gradient(135deg, rgba(255, 255, 255, 0.10) 0%, rgba(255, 255, 255, 0.05) 100%)',
        'gradient-dark': 'linear-gradient(135deg, #0f172a 0%, #064e3b 100%)',
        'gradient-teal': 'linear-gradient(135deg, #0d7377 0%, #00b8a9 100%)',
      },
      boxShadow: {
        'glass': '0 8px 32px rgba(0, 0, 0, 0.15)',
        'glass-lg': '0 20px 48px rgba(0, 0, 0, 0.25)',
        'glass-xl': '0 30px 60px rgba(0, 0, 0, 0.35)',
        'glow-success': '0 0 24px rgba(34, 197, 94, 0.25)',
        'glow-error': '0 0 24px rgba(239, 68, 68, 0.25)',
      },
      backdropBlur: {
        'xs': '4px',
      },
      borderRadius: {
        'glass': '1.5rem',
      },
      transitionDuration: {
        'fast': '200ms',
      },
    },
  },
  plugins: [],
  // Enable arbitrary values to support the exact hex colors
  safelist: [
    'bg-[#334b35]',
    'text-[#f7c35f]',
    'bg-[#f7c35f]',
    'backdrop-blur-md',
    'border-white/15',
    'border-white/20',
    'hover:bg-white/10',
    'text-white/75',
    'text-white/60',
  ]
}