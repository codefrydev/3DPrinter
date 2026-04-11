import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ["var(--font-inter)", "sans-serif"],
        mono: ["var(--font-jetbrains-mono)", "monospace"],
      },
      colors: {
        bg: "#0A0A0A",
        surface: "#171717",
        primary: "#F3F4F6",
        secondary: "#A1A1AA",
        accent: "#FFFFFF",
        syntax: {
          blue: "#93C5FD",
          green: "#86EFAC",
          pink: "#F9A8D4",
        },
      },
    },
  },
  plugins: [],
};

export default config;
