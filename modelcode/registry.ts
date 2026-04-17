import manifest from "./models.json";
import codeByFile from "./generated/codeMap";

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

function buildModels(): ModelEntry[] {
  const rows = manifest as ManifestRow[];
  return rows.map((row) => {
    const code = codeByFile[row.codeFile];
    if (typeof code !== "string") {
      throw new Error(
        `[modelcode/registry] No bundled code for codeFile "${row.codeFile}". Add modelcode/${row.codeFile}.py and run npm run sync:modelcode`,
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

/** Shown in the home hero (`CodePanel`). */
const FEATURED_MODEL_ID = "yoga-oscar";

export function getFeaturedModel(): ModelEntry {
  return getModelById(FEATURED_MODEL_ID) ?? MODELS[0];
}

export function listModelsForGallery(): GalleryModel[] {
  return MODELS.map((entry) => {
    const { code, ...rest } = entry;
    void code;
    return rest;
  });
}
