import { Box, Share2 } from "lucide-react";

export function Header() {
  return (
    <header className="flex shrink-0 items-center justify-between border-b border-[#1f1f1f] bg-bg/95 px-6 py-5 backdrop-blur lg:px-8 sticky top-0 z-50">
      <div className="flex items-center gap-2">
        <Box className="h-5 w-5 text-accent" aria-hidden />
        <span className="text-lg font-bold tracking-tight">ModelGen</span>
      </div>
      <button
        type="button"
        className="flex items-center gap-2 text-sm font-medium text-secondary transition-colors duration-200 hover:text-accent"
      >
        <Share2 className="h-4 w-4" aria-hidden />
        <span className="hidden sm:inline">Share</span>
      </button>
    </header>
  );
}
