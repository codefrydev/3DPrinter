"use client";

import { LazyModelViewer } from "@/components/LazyModelViewer";

export type GalleryCardPreviewProps = {
  src: string;
  alt: string;
};

export function GalleryCardPreview({ src, alt }: GalleryCardPreviewProps) {
  return (
    <div className="absolute inset-0">
      <LazyModelViewer
        src={src}
        alt={alt}
        className="h-full w-full"
        interactive={false}
        loading="lazy"
      />
    </div>
  );
}
