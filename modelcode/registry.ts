import homeKeyCode from "./generated/homeKey";
import manifest from "./models.json";

export type ModelTagTone = "blue" | "green" | "pink";

export type ModelEntry = {
  id: string;
  title: string;
  description: string;
  tag: string;
  tagTone: ModelTagTone;
  /** Blender version this script is written and tested against (best results). */
  blenderVersion: string;
  /** HTTPS URL to a .glb for in-browser preview only (no download UI). */
  modelUrl: string;
  code: string;
};

export type GalleryModel = Omit<ModelEntry, "code">;

type ManifestRow = {
  id: string;
  name: string;
  description: string;
  modelUrl: string;
  blenderVersion: string;
  codeFile: string;
  tag?: string;
  tagTone?: ModelTagTone;
};

const CODE_BY_FILE: Record<string, string> = {
  homeKey: homeKeyCode,
};

function buildModels(): ModelEntry[] {
  const rows = manifest as ManifestRow[];
  return rows.map((row) => {
    const code = CODE_BY_FILE[row.codeFile];
    if (typeof code !== "string") {
      throw new Error(
        `[modelcode/registry] No bundled code for codeFile "${row.codeFile}". Add import + CODE_BY_FILE entry, and ensure scripts/sync-modelcode.mjs emits modelcode/generated/${row.codeFile}.ts`,
      );
    }
    return {
      id: row.id,
      title: row.name,
      description: row.description,
      modelUrl: row.modelUrl,
      blenderVersion: row.blenderVersion,
      tag: row.tag ?? "Blender",
      tagTone: row.tagTone ?? "green",
      code,
    };
  });
}

export const MODELS: ModelEntry[] = buildModels();

export const MODEL_IDS = MODELS.map((m) => m.id);

export function getModelById(id: string): ModelEntry | undefined {
  return MODELS.find((m) => m.id === id);
}

export function getFeaturedModel(): ModelEntry {
  return MODELS[0];
}

export function listModelsForGallery(): GalleryModel[] {
  return MODELS.map((entry) => {
    const { code, ...rest } = entry;
    void code;
    return rest;
  });
}
