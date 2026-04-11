"use client";

import dynamic from "next/dynamic";
import type { ModelViewerProps } from "./ModelViewer";

export const LazyModelViewer = dynamic<ModelViewerProps>(() => import("./ModelViewer"), {
  ssr: false,
  loading: () => (
    <div
      className="relative h-full w-full overflow-hidden bg-elevated"
      role="status"
      aria-label="Loading 3D model"
    >
      <div
        className="absolute inset-0 opacity-40"
        style={{
          backgroundImage:
            "radial-gradient(circle at 50% 40%, rgb(63 63 70 / 0.35), transparent 55%)",
        }}
        aria-hidden
      />
      <div
        className="absolute inset-0 motion-safe:animate-skeleton-shimmer"
        style={{
          backgroundImage:
            "linear-gradient(105deg, transparent 35%, rgb(255 255 255 / 0.06) 50%, transparent 65%)",
          backgroundSize: "220% 100%",
        }}
        aria-hidden
      />
    </div>
  ),
});
