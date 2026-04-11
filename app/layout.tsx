import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-jetbrains-mono",
  display: "swap",
});

export const metadata: Metadata = {
  title: "ModelGen | Lunar Spacesuit",
  description:
    "Procedural 3D model showcase with generation script — ModelGen Lunar Spacesuit.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: import("react").ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.variable} ${jetbrainsMono.variable}`}>
      <body className="min-h-screen bg-bg font-sans text-primary antialiased selection:bg-accent selection:text-bg">
        {children}
      </body>
    </html>
  );
}
