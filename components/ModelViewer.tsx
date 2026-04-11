"use client";

import "@google/model-viewer";

export type ModelViewerProps = {
  src: string;
  alt: string;
  className?: string;
  /** When false, no orbit controls; pointer events pass through (e.g. card links). */
  interactive?: boolean;
  /** Viewport-based loading for thumbnails. */
  loading?: "auto" | "lazy";
};

export default function ModelViewer({
  src,
  alt,
  className,
  interactive = true,
  loading = "auto",
}: ModelViewerProps) {
  const passThrough = interactive === false;
  return (
    // Custom element from @google/model-viewer
    <model-viewer
      src={src}
      alt={alt}
      loading={loading}
      {...(interactive ? { "camera-controls": true as const } : {})}
      {...(passThrough ? { "interaction-prompt": "none" as const } : {})}
      auto-rotate
      shadow-intensity="1"
      className={
        passThrough
          ? [className, "pointer-events-none select-none"].filter(Boolean).join(" ")
          : className
      }
    />
  );
}
