"use client";

import "@google/model-viewer";

export type ModelViewerProps = {
  src: string;
  alt: string;
  className?: string;
};

export default function ModelViewer({ src, alt, className }: ModelViewerProps) {
  return (
    // Custom element from @google/model-viewer
    <model-viewer
      src={src}
      alt={alt}
      camera-controls
      auto-rotate
      shadow-intensity="1"
      className={className}
    />
  );
}
