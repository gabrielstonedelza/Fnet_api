/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Merchant+ Dark + Gold palette
        dark: {
          DEFAULT: "#0F1117",
          50: "#F1F1F4",
          100: "#D4D5DB",
          200: "#8B8FA3",
          300: "#5C6070",
          400: "#2A2E3B",
          500: "#242836",
          600: "#1A1D27",
          700: "#0F1117",
          800: "#0B0D12",
          900: "#07080B",
        },
        gold: {
          DEFAULT: "#D4A843",
          50: "#FDF8ED",
          100: "#FAEDC8",
          200: "#F5D778",
          300: "#E8C555",
          400: "#D4A843",
          500: "#C49A32",
          600: "#A68425",
          700: "#86691B",
          800: "#6B5416",
          900: "#4A3A0F",
        },
      },
    },
  },
  plugins: [],
};
