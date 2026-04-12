"use client";

import "@google/model-viewer";
import {
  DEFAULT_VIEWER_SCENE,
  VIEWER_SCENE_SOLID_BACKGROUND,
  type ViewerSceneSettings,
} from "@/lib/viewerScene";

export type ModelViewerProps = {
  src: string;
  alt: string;
  className?: string;
  /** When false, no orbit controls; pointer events pass through (e.g. card links). */
  interactive?: boolean;
  /** Viewport-based loading for thumbnails. */
  loading?: "auto" | "lazy";
  /** Lighting, shadows, and background; defaults match site defaults. */
  scene?: ViewerSceneSettings;
};

export default function ModelViewer({
  src,
  alt,
  className,
  interactive = true,
  loading = "auto",
  scene: sceneProp,
}: ModelViewerProps) {
  const passThrough = interactive === false;
  const scene = sceneProp ?? DEFAULT_VIEWER_SCENE;
  const bg = scene.backgroundTransparent ? "transparent" : VIEWER_SCENE_SOLID_BACKGROUND;

  return (
    <model-viewer
      src={src}
      alt={alt}
      loading={loading}
      {...(interactive ? { "camera-controls": true as const } : {})}
      {...(passThrough ? { "interaction-prompt": "none" as const } : {})}
      auto-rotate
      environment-image={scene.environmentImage}
      exposure={String(scene.exposure)}
      shadow-intensity={String(scene.shadowIntensity)}
      shadow-softness={String(scene.shadowSoftness)}
      style={{ backgroundColor: bg }}
      className={
        passThrough
          ? [className, "pointer-events-none select-none"].filter(Boolean).join(" ")
          : className
      }
    />
  );
}
