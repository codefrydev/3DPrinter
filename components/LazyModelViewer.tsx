"use client";

import dynamic from "next/dynamic";

export const LazyModelViewer = dynamic(() => import("./ModelViewer"), {
  ssr: false,
  loading: () => (
    <div
      className="h-full w-full bg-[#121212]"
      aria-hidden
    />
  ),
});
