"use client";

import { useCallback, useState } from "react";
import { Check, Copy, Mouse } from "lucide-react";
import type { ModelEntry } from "@/modelcode/registry";
import { LazyModelViewer } from "@/components/LazyModelViewer";
import { copyToClipboard } from "@/lib/copyToClipboard";

export type CodePanelProps = {
  model: ModelEntry;
};

function ModelStage({ model }: { model: ModelEntry }) {
  const [overlayCopied, setOverlayCopied] = useState(false);

  const handleOverlayCopy = useCallback(async () => {
    if (overlayCopied) return;
    const ok = await copyToClipboard(model.code);
    if (!ok) return;
    setOverlayCopied(true);
    window.setTimeout(() => setOverlayCopied(false), 2000);
  }, [overlayCopied, model.code]);

  return (
    <section
      className="relative flex h-[55vh] w-full shrink-0 items-center justify-center p-4 lg:h-auto lg:w-1/2 lg:p-8"
      aria-label="Interactive 3D preview"
    >
      <div className="group relative h-full w-full overflow-hidden rounded-stage border border-line bg-gradient-to-b from-inset to-bg shadow-stage">
        <div
          className="pointer-events-none absolute inset-0 opacity-[0.35]"
          style={{
            backgroundImage:
              "radial-gradient(ellipse 80% 60% at 50% 45%, rgb(39 39 42 / 0.45), transparent 65%)",
          }}
          aria-hidden
        />

        <div className="absolute right-4 top-4 z-10 translate-y-[-8px] opacity-0 transition-all duration-300 ease-out group-hover:translate-y-0 group-hover:opacity-100 motion-reduce:translate-y-0 motion-reduce:opacity-100 motion-reduce:transition-none">
          <button
            type="button"
            onClick={handleOverlayCopy}
            aria-pressed={overlayCopied}
            className="flex items-center gap-2 rounded-control border border-line-strong bg-surface/85 px-3.5 py-2 text-sm font-medium text-primary shadow-card backdrop-blur-sm transition-colors hover:border-line-focus hover:bg-surface motion-reduce:transition-none"
          >
            {overlayCopied ? (
              <Check className="h-4 w-4 text-syntax-green" aria-hidden />
            ) : (
              <Copy className="h-4 w-4" aria-hidden />
            )}
            <span>{overlayCopied ? "Copied" : "Copy code"}</span>
          </button>
        </div>

        <span className="sr-only" aria-live="polite">
          {overlayCopied ? "Code copied to clipboard." : ""}
        </span>

        <div className="absolute inset-0">
          <LazyModelViewer
            src={model.modelUrl}
            alt={`${model.title} — 3D preview`}
            className="h-full w-full"
          />
        </div>

        <div className="pointer-events-none absolute bottom-4 left-1/2 flex max-w-[90%] -translate-x-1/2 flex-col items-center gap-1 rounded-full border border-line-strong bg-surface/85 px-3 py-1.5 text-center text-xs text-secondary shadow-card backdrop-blur-sm opacity-80 transition-opacity duration-300 ease-out group-hover:opacity-100 motion-reduce:opacity-100 motion-reduce:transition-none">
          <span className="flex items-center gap-2">
            <Mouse className="h-3 w-3 shrink-0 text-secondary" aria-hidden />
            Scroll to zoom · drag to rotate
          </span>
          <span className="text-[10px] font-normal text-secondary/90">
            Web preview only — no file download from this page.
          </span>
        </div>
      </div>
    </section>
  );
}

function HeroCopy({ model }: { model: ModelEntry }) {
  return (
    <div className="mb-10 max-w-measure">
      <p className="mb-3 text-xs font-medium uppercase tracking-[0.2em] text-secondary">
        {model.tag}
      </p>
      <h1
        id="showcase-heading"
        className="mb-4 text-3xl font-semibold tracking-tight text-primary sm:text-4xl"
      >
        {model.title}
      </h1>
      <p className="mb-3 rounded-control border border-line-strong bg-elevated px-3 py-2 text-sm text-secondary">
        <span className="font-medium text-primary">Blender {model.blenderVersion}</span>
        <span className="text-secondary"> — use this version for best results when running the script.</span>
      </p>
      <p className="text-base font-light leading-relaxed text-secondary sm:text-lg">
        {model.description}
      </p>
    </div>
  );
}

function HeroActions({ model }: { model: ModelEntry }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = useCallback(async () => {
    if (copied) return;
    const ok = await copyToClipboard(model.code);
    if (!ok) return;
    setCopied(true);
    window.setTimeout(() => setCopied(false), 2000);
  }, [copied, model.code]);

  return (
    <div className="mt-10 flex flex-col items-stretch gap-3">
      <button
        type="button"
        onClick={handleCopy}
        aria-pressed={copied}
        className="inline-flex w-full items-center justify-center gap-2 rounded-control bg-accent px-6 py-3 text-sm font-semibold text-bg shadow-card transition-colors hover:bg-primary active:scale-[0.99] motion-reduce:active:scale-100 sm:w-auto sm:self-start"
      >
        {copied ? (
          <Check className="h-4 w-4 text-emerald-700" aria-hidden />
        ) : (
          <Copy className="h-4 w-4" aria-hidden />
        )}
        {copied ? "Copied to clipboard" : "Copy generation code"}
      </button>
      <span className="sr-only" aria-live="polite">
        {copied ? "Code copied to clipboard." : ""}
      </span>
    </div>
  );
}

export function CodePanel({ model }: CodePanelProps) {
  return (
    <div
      id="showcase"
      className="flex min-h-[calc(100vh-73px)] flex-col border-b border-line lg:flex-row"
    >
      <ModelStage model={model} />
      <section className="flex w-full flex-col justify-center p-6 lg:w-1/2 lg:p-12 lg:pl-6">
        <div className="mx-auto flex w-full max-w-measure flex-col lg:mx-0">
          <HeroCopy model={model} />
          <HeroActions model={model} />
        </div>
      </section>
    </div>
  );
}
