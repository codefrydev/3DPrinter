"use client";

import { useState } from "react";
import { ChevronDown, Cog } from "lucide-react";
import {
  VIEWER_SCENE_PRESETS,
  type ViewerScenePresetId,
} from "@/lib/viewerScene";
import { useViewerScene } from "@/components/ViewerSceneProvider";

const PRESET_LABELS: Record<ViewerScenePresetId, string> = {
  neutralStudio: "Neutral studio",
  legacyFront: "Legacy",
  softProduct: "Soft product",
};

export function ViewerEnvironmentControls() {
  const { scene, setScene, updateScene } = useViewerScene();
  const [minimized, setMinimized] = useState(true);

  return (
    <div
      className={`absolute bottom-4 left-4 z-10 max-w-[min(100%,18rem)] rounded-control border border-line-strong bg-surface/85 shadow-card backdrop-blur-sm ${
        minimized ? "p-1.5" : "p-3"
      }`}
      role="group"
      aria-label="3D scene and lighting"
    >
      {minimized ? (
        <button
          type="button"
          onClick={() => setMinimized(false)}
          aria-expanded={false}
          aria-controls="viewer-scene-controls-body"
          className="flex h-9 w-9 items-center justify-center rounded border border-transparent text-secondary transition-colors hover:border-line hover:bg-elevated hover:text-primary"
          title="Scene settings"
          aria-label="Open scene settings"
        >
          <Cog className="h-5 w-5" aria-hidden strokeWidth={1.75} />
        </button>
      ) : (
        <>
          <div className="flex items-center justify-between gap-2">
            <p className="text-xs font-medium uppercase tracking-[0.12em] text-secondary">Scene</p>
            <button
              type="button"
              onClick={() => setMinimized(true)}
              aria-expanded={true}
              aria-controls="viewer-scene-controls-body"
              className="flex h-7 w-7 shrink-0 items-center justify-center rounded border border-line text-secondary transition-colors hover:border-line-focus hover:bg-elevated hover:text-primary"
              title="Minimize scene controls"
              aria-label="Minimize scene controls"
            >
              <ChevronDown className="h-4 w-4" aria-hidden />
            </button>
          </div>

          <div id="viewer-scene-controls-body" className="mt-2">
            <div className="mb-3 flex flex-wrap gap-1.5">
              {(Object.keys(VIEWER_SCENE_PRESETS) as ViewerScenePresetId[]).map((id) => (
                <button
                  key={id}
                  type="button"
                  onClick={() => setScene(VIEWER_SCENE_PRESETS[id])}
                  className="rounded border border-line px-2 py-1 text-xs font-medium text-primary transition-colors hover:border-line-focus hover:bg-elevated"
                >
                  {PRESET_LABELS[id]}
                </button>
              ))}
            </div>

            <div className="space-y-2.5">
              <label className="flex flex-col gap-1 text-xs text-secondary">
                <span className="flex justify-between gap-2 text-muted">
                  <span>Exposure</span>
                  <span className="tabular-nums text-secondary">{scene.exposure.toFixed(2)}</span>
                </span>
                <input
                  type="range"
                  min={0.5}
                  max={2.5}
                  step={0.05}
                  value={scene.exposure}
                  onChange={(e) => updateScene({ exposure: Number(e.target.value) })}
                  className="h-1.5 w-full cursor-pointer accent-accent"
                />
              </label>

              <label className="flex flex-col gap-1 text-xs text-secondary">
                <span className="flex justify-between gap-2 text-muted">
                  <span>Shadow</span>
                  <span className="tabular-nums text-secondary">{scene.shadowIntensity.toFixed(2)}</span>
                </span>
                <input
                  type="range"
                  min={0}
                  max={1}
                  step={0.05}
                  value={scene.shadowIntensity}
                  onChange={(e) => updateScene({ shadowIntensity: Number(e.target.value) })}
                  className="h-1.5 w-full cursor-pointer accent-accent"
                />
              </label>

              <label className="flex flex-col gap-1 text-xs text-secondary">
                <span className="flex justify-between gap-2 text-muted">
                  <span>Shadow softness</span>
                  <span className="tabular-nums text-secondary">{scene.shadowSoftness.toFixed(2)}</span>
                </span>
                <input
                  type="range"
                  min={0}
                  max={2}
                  step={0.05}
                  value={scene.shadowSoftness}
                  onChange={(e) => updateScene({ shadowSoftness: Number(e.target.value) })}
                  className="h-1.5 w-full cursor-pointer accent-accent"
                />
              </label>

              <label className="flex cursor-pointer items-center gap-2 text-xs text-secondary">
                <input
                  type="checkbox"
                  checked={scene.backgroundTransparent}
                  onChange={(e) => updateScene({ backgroundTransparent: e.target.checked })}
                  className="h-3.5 w-3.5 rounded border-line text-accent focus:ring-line-focus"
                />
                <span>Transparent background</span>
              </label>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
