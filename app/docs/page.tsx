import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Documentation",
  description:
    "How to browse models, use the 3D viewer, copy Blender scripts, and adjust scene lighting in 3D Printer.",
  openGraph: {
    title: "Documentation",
    description:
      "How to browse models, use the 3D viewer, copy Blender scripts, and adjust scene lighting in 3D Printer.",
  },
};

export default function DocsPage() {
  return (
    <main
      id="main-content"
      className="mx-auto max-w-measure px-6 py-16 lg:px-8"
    >
      <p className="mb-4 text-xs font-medium uppercase tracking-[0.2em] text-secondary">
        Guide
      </p>
      <h1 className="mb-6 text-3xl font-semibold tracking-tight text-primary sm:text-4xl">
        Documentation
      </h1>
      <p className="mb-12 text-base font-light leading-relaxed text-secondary sm:text-lg">
        3D Printer is a procedural model showcase: browse GLB previews in the browser and copy
        generation scripts to run in Blender.
      </p>

      <div className="space-y-12 text-secondary">
        <section aria-labelledby="docs-browse">
          <h2
            id="docs-browse"
            className="mb-3 text-lg font-semibold tracking-tight text-primary"
          >
            Browse and open a model
          </h2>
          <p className="leading-relaxed">
            On the home page, the <strong className="font-medium text-primary">Showcase</strong>{" "}
            highlights a featured model; scroll to the <strong className="font-medium text-primary">Gallery</strong>{" "}
            for the full collection. Click a card to open its viewer page with a larger preview and
            copy actions.
          </p>
        </section>

        <section aria-labelledby="docs-copy">
          <h2
            id="docs-copy"
            className="mb-3 text-lg font-semibold tracking-tight text-primary"
          >
            Copy generation code
          </h2>
          <p className="leading-relaxed">
            Each viewer page includes <strong className="font-medium text-primary">Copy generation code</strong>, which
            copies the bundled Blender/Python script to your clipboard. A version callout shows which{" "}
            <strong className="font-medium text-primary">Blender</strong> release the script is written
            for—use that version for the most reliable results. On desktop, you can also use{" "}
            <strong className="font-medium text-primary">Copy code</strong> over the 3D preview.
          </p>
        </section>

        <section aria-labelledby="docs-viewer">
          <h2
            id="docs-viewer"
            className="mb-3 text-lg font-semibold tracking-tight text-primary"
          >
            3D viewer and scene controls
          </h2>
          <ul className="list-disc space-y-2 pl-5 leading-relaxed">
            <li>
              <strong className="font-medium text-primary">Orbit:</strong> drag to rotate the model
              (when interactive). Auto-rotate may be enabled unless your system prefers reduced motion.
            </li>
            <li>
              <strong className="font-medium text-primary">Scene</strong> (cog): choose a lighting
              preset (Neutral studio, Legacy, Soft product), adjust exposure, shadow intensity and
              softness, or toggle a transparent background so the page gradient shows through.
            </li>
            <li>
              Scene settings are remembered in your browser for the next visit.
            </li>
          </ul>
        </section>

        <section aria-labelledby="docs-share">
          <h2
            id="docs-share"
            className="mb-3 text-lg font-semibold tracking-tight text-primary"
          >
            Share
          </h2>
          <p className="leading-relaxed">
            Use <strong className="font-medium text-primary">Share</strong> in the header to open the
            system share sheet where supported, or copy the current page URL to the clipboard.
          </p>
        </section>

        <p className="border-t border-line pt-8 text-sm">
          <Link
            href="/"
            className="font-medium text-primary underline-offset-4 transition-colors hover:text-accent hover:underline"
          >
            Back to home
          </Link>
        </p>
      </div>
    </main>
  );
}
