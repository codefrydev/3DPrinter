"use client";

import { useCallback, useState } from "react";
import Link from "next/link";
import { Box, Check, Share2 } from "lucide-react";
import { copyToClipboard } from "@/lib/copyToClipboard";

type ShareFeedback = "idle" | "copied" | "shared";

const navLinkClass =
  "transition-colors hover:text-primary motion-reduce:transition-none";

const primaryLinks = (
  <>
    <li>
      <Link href="/#showcase" className={navLinkClass}>
        Showcase
      </Link>
    </li>
    <li>
      <Link href="/#gallery" className={navLinkClass}>
        Gallery
      </Link>
    </li>
    <li>
      <Link href="/docs/" className={navLinkClass}>
        Documentation
      </Link>
    </li>
  </>
);

export function Header() {
  const [feedback, setFeedback] = useState<ShareFeedback>("idle");

  const handleShare = useCallback(async () => {
    if (feedback !== "idle") return;
    const url =
      typeof window !== "undefined" ? window.location.href : "";

    if (navigator.share && url) {
      try {
        await navigator.share({
          title: document.title,
          url,
        });
        setFeedback("shared");
        window.setTimeout(() => setFeedback("idle"), 2000);
        return;
      } catch (e) {
        if (e instanceof DOMException && e.name === "AbortError") return;
      }
    }

    const ok = await copyToClipboard(url);
    if (!ok) return;
    setFeedback("copied");
    window.setTimeout(() => setFeedback("idle"), 2000);
  }, [feedback]);

  return (
    <header className="sticky top-0 z-50 shrink-0 border-b border-line bg-bg/90 px-6 py-4 backdrop-blur-md lg:px-8">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:gap-6 lg:gap-8">
        <div className="flex items-center justify-between gap-4 sm:contents">
          <Link
            href="/"
            className="order-1 flex min-w-0 shrink-0 items-center gap-2 sm:order-1"
          >
            <Box className="h-5 w-5 shrink-0 text-accent" aria-hidden />
            <span className="text-lg font-semibold tracking-tight text-primary">
              3D Printer
            </span>
          </Link>
          <button
            type="button"
            onClick={handleShare}
            aria-label={
              feedback === "copied"
                ? "Page link copied"
                : feedback === "shared"
                  ? "Share sheet completed"
                  : "Share or copy page link"
            }
            className="order-2 inline-flex shrink-0 flex-row items-center gap-2 rounded-control border border-transparent px-3 py-2 text-sm font-medium text-secondary transition-colors hover:border-line-strong hover:bg-surface/60 hover:text-primary motion-reduce:transition-none sm:order-3"
            aria-live="polite"
          >
            {feedback !== "idle" ? (
              <Check className="h-4 w-4 shrink-0 text-syntax-green" aria-hidden />
            ) : (
              <Share2 className="h-4 w-4 shrink-0" aria-hidden />
            )}
            <span className="hidden sm:inline">
              {feedback === "copied"
                ? "Link copied"
                : feedback === "shared"
                  ? "Shared"
                  : "Share"}
            </span>
          </button>
        </div>

        <nav
          aria-label="Primary"
          className="order-3 w-full max-sm:border-t max-sm:border-line/80 max-sm:pt-3 sm:order-2 sm:min-w-0 sm:flex-1"
        >
          <ul className="flex list-none flex-wrap items-center gap-x-6 gap-y-2 text-sm font-medium text-secondary sm:justify-center">
            {primaryLinks}
          </ul>
        </nav>
      </div>
    </header>
  );
}
