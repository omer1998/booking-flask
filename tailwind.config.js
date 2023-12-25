/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors')
module.exports = {
  content: [
    "./templates/**/*.{html,js}",
    'node_modules/preline/dist/*.js',
  ],
  theme: {
    extend: {
      colors: {
        "primary-c": {
          100: 'var(--primary-100)',
          200: 'var(--primary-200)'
        },
        "accent-c": {
          100: "#46B77B",
          200: "#ffe4ff"
        },
        "text-c": "#333333"
      }
    },
    
  },
  plugins: [
    require('preline/plugin'),

  ],
  // safelist: [
  //   {
  //     pattern:
  //       /(bg|text|border)-(primary-c|accent-c|text-c)/,
  //   },
  // ],
  
}

// --primary - 200:#757de8;
// --primary - 300: #dedeff;
// --accent - 100: #fe6e9e;
// --accent - 200: #ffe4ff;
// --text - 100:#333333;
// --text - 200:#5c5c5c;
// --bg - 100: #F5F5F5;
// --bg - 200: #ebebeb;
// --bg - 300: #c2c2c2;