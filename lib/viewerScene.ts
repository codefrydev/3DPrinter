export type ViewerEnvironmentImage = "neutral" | "legacy";

export type ViewerSceneSettings = {
  environmentImage: ViewerEnvironmentImage;
  exposure: number;
  shadowIntensity: number;
  shadowSoftness: number;
  /** When true, the viewer background is transparent so the page gradient shows through. */
  backgroundTransparent: boolean;
};

export const VIEWER_SCENE_STORAGE_KEY = "modelgen-viewer-scene";

export const DEFAULT_VIEWER_SCENE: ViewerSceneSettings = {
  environmentImage: "neutral",
  exposure: 1,
  shadowIntensity: 1,
  shadowSoftness: 1,
  backgroundTransparent: true,
};

const ELEVATED_SOLID = "#121212";

export const VIEWER_SCENE_SOLID_BACKGROUND = ELEVATED_SOLID;

export type ViewerScenePresetId = "neutralStudio" | "legacyFront" | "softProduct";

export const VIEWER_SCENE_PRESETS: Record<ViewerScenePresetId, ViewerSceneSettings> = {
  neutralStudio: {
    environmentImage: "neutral",
    exposure: 1,
    shadowIntensity: 1,
    shadowSoftness: 1,
    backgroundTransparent: true,
  },
  legacyFront: {
    environmentImage: "legacy",
    exposure: 1,
    shadowIntensity: 1,
    shadowSoftness: 1,
    backgroundTransparent: true,
  },
  softProduct: {
    environmentImage: "neutral",
    exposure: 1.1,
    shadowIntensity: 0.65,
    shadowSoftness: 1.4,
    backgroundTransparent: true,
  },
};

function clamp(n: number, min: number, max: number): number {
  return Math.min(max, Math.max(min, n));
}

export function mergeViewerScene(partial: unknown): ViewerSceneSettings {
  const base: ViewerSceneSettings = { ...DEFAULT_VIEWER_SCENE };
  if (!partial || typeof partial !== "object") return base;
  const o = partial as Record<string, unknown>;

  if (o.environmentImage === "neutral" || o.environmentImage === "legacy") {
    base.environmentImage = o.environmentImage;
  }
  if (typeof o.exposure === "number" && Number.isFinite(o.exposure)) {
    base.exposure = clamp(o.exposure, 0.5, 2.5);
  }
  if (typeof o.shadowIntensity === "number" && Number.isFinite(o.shadowIntensity)) {
    base.shadowIntensity = clamp(o.shadowIntensity, 0, 1);
  }
  if (typeof o.shadowSoftness === "number" && Number.isFinite(o.shadowSoftness)) {
    base.shadowSoftness = clamp(o.shadowSoftness, 0, 2);
  }
  if (typeof o.backgroundTransparent === "boolean") {
    base.backgroundTransparent = o.backgroundTransparent;
  }

  return base;
}

export function loadViewerSceneFromStorage(): ViewerSceneSettings | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = localStorage.getItem(VIEWER_SCENE_STORAGE_KEY);
    if (!raw) return null;
    return mergeViewerScene(JSON.parse(raw));
  } catch {
    return null;
  }
}

export function saveViewerSceneToStorage(scene: ViewerSceneSettings): void {
  if (typeof window === "undefined") return;
  try {
    localStorage.setItem(VIEWER_SCENE_STORAGE_KEY, JSON.stringify(scene));
  } catch {
    /* quota / private mode */
  }
}
