"use client";

import { useCallback, useState } from "react";
import { Check, Copy, Download, Mouse } from "lucide-react";
import { LUNAR_SPACESUIT_CODE } from "@/lib/modelgenCode";
import { LazyModelViewer } from "@/components/LazyModelViewer";

const MODEL_SRC =
  "https://modelviewer.dev/shared-assets/models/Astronaut.glb";

async function copyToClipboard(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    try {
      const ta = document.createElement("textarea");
      ta.value = text;
      ta.setAttribute("readonly", "");
      ta.style.position = "fixed";
      ta.style.left = "-9999px";
      document.body.appendChild(ta);
      ta.select();
      const ok = document.execCommand("copy");
      document.body.removeChild(ta);
      return ok;
    } catch {
      return false;
    }
  }
}

function ModelStage() {
  const [overlayCopied, setOverlayCopied] = useState(false);

  const handleOverlayCopy = useCallback(async () => {
    if (overlayCopied) return;
    const ok = await copyToClipboard(LUNAR_SPACESUIT_CODE);
    if (!ok) return;
    setOverlayCopied(true);
    window.setTimeout(() => setOverlayCopied(false), 2000);
  }, [overlayCopied]);

  return (
    <section className="relative flex h-[55vh] w-full shrink-0 items-center justify-center p-4 lg:h-auto lg:w-1/2 lg:p-8">
      <div className="group relative h-full w-full overflow-hidden rounded-lg border border-[#1f1f1f] bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-[#1a1a1a] to-bg">
        <div className="absolute right-4 top-4 z-10 translate-y-[-10px] opacity-0 transition-all duration-300 group-hover:translate-y-0 group-hover:opacity-100">
          <button
            type="button"
            onClick={handleOverlayCopy}
            className="flex items-center gap-2 rounded-lg border border-[#27272a] bg-surface/80 px-4 py-2 text-sm font-medium text-primary shadow-lg backdrop-blur transition-all hover:border-secondary hover:bg-surface"
          >
            {overlayCopied ? (
              <Check className="h-4 w-4 text-syntax-green" aria-hidden />
            ) : (
              <Copy className="h-4 w-4" aria-hidden />
            )}
            <span>{overlayCopied ? "Copied!" : "Copy Code"}</span>
          </button>
        </div>

        <div className="absolute inset-0">
          <LazyModelViewer
            src={MODEL_SRC}
            alt="Lunar spacesuit showcase model"
            className="h-full w-full"
          />
        </div>

        <div className="pointer-events-none absolute bottom-4 left-1/2 flex -translate-x-1/2 items-center gap-2 rounded-full border border-[#27272a] bg-surface/80 px-3 py-1.5 text-xs text-secondary opacity-0 backdrop-blur transition-opacity duration-300 group-hover:opacity-100">
          <Mouse className="h-3 w-3" aria-hidden />
          Scroll to zoom, drag to rotate
        </div>
      </div>
    </section>
  );
}

function HeroCopy() {
  return (
    <div className="mb-8">
      <h1 className="mb-3 text-3xl font-bold tracking-tight lg:text-4xl">
        Lunar Spacesuit
      </h1>
      <p className="font-light leading-relaxed text-secondary">
        A highly detailed procedural generation script for the Artemis-class
        extravehicular mobility unit. Rendered in real-time.
      </p>
    </div>
  );
}

function HeroActions() {
  return (
    <div className="mt-8 flex flex-col items-center gap-4 sm:flex-row">
      <button
        type="button"
        className="flex w-full items-center justify-center gap-2 rounded bg-accent px-6 py-3 text-sm font-semibold text-bg transition-colors hover:bg-gray-200 sm:w-auto"
      >
        <Download className="h-4 w-4" aria-hidden />
        Download .glb
      </button>
      <a
        href="#"
        className="w-full py-3 text-center text-sm text-secondary transition-colors hover:text-accent sm:w-auto"
      >
        View Documentation
      </a>
    </div>
  );
}

export function CodePanel() {
  return (
    <div className="flex min-h-[calc(100vh-73px)] flex-col border-b border-[#1f1f1f] lg:flex-row">
      <ModelStage />
      <section className="flex w-full flex-col p-6 lg:w-1/2 lg:p-12 lg:pl-4">
        <div className="mx-auto flex w-full max-w-2xl flex-col lg:mx-0">
          <HeroCopy />
          <HeroActions />
        </div>
      </section>
    </div>
  );
}
