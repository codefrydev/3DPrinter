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
      maxWidth: {
        measure: "42rem",
      },
      borderRadius: {
        card: "0.5rem",
        stage: "0.5rem",
        control: "0.375rem",
      },
      boxShadow: {
        card: "0 10px 40px -12px rgb(0 0 0 / 0.55)",
        "card-hover": "0 14px 48px -10px rgb(0 0 0 / 0.6)",
        stage:
          "inset 0 0 0 1px rgb(255 255 255 / 0.04), 0 28px 56px -28px rgb(0 0 0 / 0.65)",
      },
      keyframes: {
        "skeleton-shimmer": {
          "0%": { backgroundPosition: "200% 0" },
          "100%": { backgroundPosition: "-200% 0" },
        },
      },
      animation: {
        "skeleton-shimmer": "skeleton-shimmer 2.2s ease-in-out infinite",
      },
      colors: {
        bg: "#0A0A0A",
        surface: "#171717",
        elevated: "#121212",
        muted: "#141414",
        inset: "#1A1A1A",
        line: "#1F1F1F",
        "line-strong": "#27272A",
        "line-focus": "#3F3F46",
        primary: "#F3F4F6",
        secondary: "#B4B4BC",
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
