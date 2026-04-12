import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import { Footer } from "@/components/Footer";
import { Header } from "@/components/Header";
import { ViewerSceneProvider } from "@/components/ViewerSceneProvider";
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

const siteUrl =
  process.env.NEXT_PUBLIC_SITE_URL != null && process.env.NEXT_PUBLIC_SITE_URL !== ""
    ? process.env.NEXT_PUBLIC_SITE_URL
    : "http://localhost:3000";

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  title: {
    default: "3D Printer",
    template: "%s | 3D Printer",
  },
  description:
    "Procedural 3D model showcase: browse scripts, preview GLBs in the browser, and copy generation code.",
  openGraph: {
    title: "3D Printer",
    description:
      "Procedural 3D model showcase: browse scripts, preview GLBs in the browser, and copy generation code.",
    type: "website",
    images: [
      {
        url: "/og.png",
        width: 1200,
        height: 630,
        alt: "3D Printer",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "3D Printer",
    description:
      "Procedural 3D model showcase: browse scripts, preview GLBs in the browser, and copy generation code.",
    images: ["/og.png"],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: import("react").ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.variable} ${jetbrainsMono.variable}`}>
      <body className="min-h-screen bg-bg font-sans text-primary antialiased selection:bg-accent selection:text-bg">
        <a href="#main-content" className="skip-link">
          Skip to main content
        </a>
        <ViewerSceneProvider>
          <div className="flex min-h-screen flex-col">
            <Header />
            <div className="flex-1">{children}</div>
            <Footer />
          </div>
        </ViewerSceneProvider>
      </body>
    </html>
  );
}
