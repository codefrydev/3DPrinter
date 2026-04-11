"use client";

import { useCallback, useState } from "react";
import { Box, Check, Share2 } from "lucide-react";
import { copyToClipboard } from "@/lib/copyToClipboard";

type ShareFeedback = "idle" | "copied" | "shared";

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
    <header className="sticky top-0 z-50 flex shrink-0 items-center justify-between border-b border-line bg-bg/90 px-6 py-4 backdrop-blur-md lg:px-8">
      <div className="flex items-center gap-8">
        <div className="flex items-center gap-2">
          <Box className="h-5 w-5 text-accent" aria-hidden />
          <span className="text-lg font-semibold tracking-tight text-primary">
            ModelGen
          </span>
        </div>
        <nav className="hidden items-center gap-6 text-sm font-medium text-secondary sm:flex">
          <a
            href="#showcase"
            className="transition-colors hover:text-primary motion-reduce:transition-none"
          >
            Showcase
          </a>
          <a
            href="#gallery"
            className="transition-colors hover:text-primary motion-reduce:transition-none"
          >
            Gallery
          </a>
        </nav>
      </div>
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
        className="flex items-center gap-2 rounded-control border border-transparent px-3 py-2 text-sm font-medium text-secondary transition-colors hover:border-line-strong hover:bg-surface/60 hover:text-primary motion-reduce:transition-none"
        aria-live="polite"
      >
        {feedback !== "idle" ? (
          <Check className="h-4 w-4 text-syntax-green" aria-hidden />
        ) : (
          <Share2 className="h-4 w-4" aria-hidden />
        )}
        <span className="hidden sm:inline">
          {feedback === "copied"
            ? "Link copied"
            : feedback === "shared"
              ? "Shared"
              : "Share"}
        </span>
      </button>
    </header>
  );
}
