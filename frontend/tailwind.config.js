/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        cyber: {
          bg: '#070D18',
          card: '#0E1726',
          border: 'rgba(0, 229, 255, 0.16)',
          cyan: '#00E5FF',
          emerald: '#00E676',
          blue: '#2979FF',
          muted: '#94A3B8',
          darkBlue: '#0F2744',
        },
        slateTheme: {
          bg: '#1E2538',
          card: '#283149',
          border: 'rgba(255, 255, 255, 0.08)',
          cyan: '#38BDF8',
          emerald: '#34D399',
        }
      },
      fontFamily: {
        sans: ['Plus Jakarta Sans', 'Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 10px rgba(0, 229, 255, 0.2)' },
          '100%': { boxShadow: '0 0 25px rgba(0, 229, 255, 0.6)' },
        }
      }
    },
  },
  plugins: [],
}
