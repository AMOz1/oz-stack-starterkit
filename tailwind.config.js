/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/templates/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["light", "dark"],
  },
};