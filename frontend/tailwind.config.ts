import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#ecf9ff',
          100: '#d8f0ff',
          200: '#aee0ff',
          300: '#7cccff',
          400: '#33b0ff',
          500: '#0b94f5',
          600: '#0073d1',
          700: '#005aa6',
          800: '#00417a',
          900: '#012f5c'
        }
      }
    }
  },
  plugins: []
};

export default config;
