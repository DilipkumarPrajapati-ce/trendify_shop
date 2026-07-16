/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#fff9f7',
          100: '#fff3ef',
          500: '#C9A227',
          700: '#b38f1f'
        }
      }
    }
  },
  plugins: [],
}
