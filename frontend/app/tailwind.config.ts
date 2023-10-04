const defaultTheme = require("tailwindcss/defaultTheme");

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Lato", ...defaultTheme.fontFamily.sans],
      },
      colors: {
        primary: "#16BAC5",
        secondary: "#5FBFF9",
        background: {
          light: "#EFE9F4",
          DEFAULT: "#EFE9F4",
          dark: "#171D1C",
        },
        font: {
          DEFAULT: "#111111",
          title: "#2C2948",
          subtitle: "#6E7191",
          input: "#14142B",
        },
        error: "#EB5757",
        accent: "#FB7A08",
        body: "#4E4B66",
      },
      display: ["group-hover"],
      maxHeight: {
        "3-lines": "4.5rem",
      },
    },
  },
  plugins: [],
};