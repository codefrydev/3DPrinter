import Link from "next/link";
import { ArrowRight, Box, Home } from "lucide-react";
import type { GalleryModel, ModelTagTone } from "@/modelcode/registry";
import type { LucideIcon } from "lucide-react";

const toneClass: Record<ModelTagTone, string> = {
  blue: "text-syntax-blue",
  green: "text-syntax-green",
  pink: "text-syntax-pink",
};

const iconById: Record<string, LucideIcon> = {
  "home-key": Home,
};

function cardIcon(id: string): LucideIcon {
  return iconById[id] ?? Box;
}

export type GalleryProps = {
  models: readonly GalleryModel[];
};

export function Gallery({ models }: GalleryProps) {
  return (
    <section
      id="gallery"
      className="mx-auto max-w-7xl scroll-mt-24 px-6 py-20 lg:px-8"
      aria-labelledby="gallery-heading"
    >
      <div className="mb-12 flex flex-col items-start justify-between gap-6 sm:flex-row sm:items-end">
        <div className="max-w-measure">
          <h2
            id="gallery-heading"
            className="mb-2 text-2xl font-semibold tracking-tight text-primary"
          >
            Procedural collection
          </h2>
          <p className="font-light leading-relaxed text-secondary">
            Open a viewer page for the 3D preview, then copy the Blender or
            script source from there.
          </p>
        </div>
        <a
          href="#gallery"
          className="group inline-flex items-center gap-2 rounded-control border border-transparent px-3 py-2 text-sm font-medium text-secondary transition-colors hover:border-line-strong hover:text-primary motion-reduce:transition-none"
        >
          Browse models
          <ArrowRight
            className="h-4 w-4 transition-transform duration-200 ease-out group-hover:translate-x-0.5 motion-reduce:transition-none"
            aria-hidden
          />
        </a>
      </div>

      <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        {models.map((m) => {
          const Icon = cardIcon(m.id);
          const tagClass = toneClass[m.tagTone];
          return (
            <Link
              key={m.id}
              href={`/view/${m.id}/`}
              aria-label={`${m.title}: open 3D viewer and copy code. ${m.description}`}
              className="group block overflow-hidden rounded-card border border-line-strong bg-surface shadow-card transition-[border-color,box-shadow,transform] duration-300 ease-out hover:-translate-y-0.5 hover:border-line-focus hover:shadow-card-hover motion-reduce:transition-none motion-reduce:hover:translate-y-0"
            >
              <div className="relative flex h-52 items-center justify-center overflow-hidden border-b border-line-strong bg-elevated">
                <div
                  className="absolute inset-0 opacity-50"
                  style={{
                    backgroundImage:
                      "radial-gradient(circle at center, rgb(39 39 42 / 0.5), transparent 70%)",
                  }}
                  aria-hidden
                />
                <Icon className="relative z-10 h-12 w-12 text-line-focus transition-colors duration-300 ease-out group-hover:text-secondary motion-reduce:transition-none" />
              </div>
              <div className="p-6">
                <div className="mb-3 flex items-start justify-between gap-3">
                  <h3 className="font-semibold text-primary transition-colors duration-200 group-hover:text-accent motion-reduce:transition-none">
                    {m.title}
                  </h3>
                  <span
                    className={`shrink-0 rounded border border-line-strong bg-elevated px-2 py-1 font-mono text-[10px] font-medium uppercase tracking-wide ${tagClass}`}
                  >
                    {m.tag}
                  </span>
                </div>
                <p className="line-clamp-3 text-sm leading-relaxed text-secondary">
                  {m.description}
                </p>
                <p className="mt-3 font-mono text-[10px] text-secondary/90">
                  Blender {m.blenderVersion}
                </p>
                <p className="mt-2 text-xs font-medium text-accent/80">
                  Open viewer →
                </p>
              </div>
            </Link>
          );
        })}
      </div>
    </section>
  );
}
