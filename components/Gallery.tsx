import { ArrowRight, Cpu, Dna, MountainSnow } from "lucide-react";

const cards = [
  {
    href: "#",
    title: "Quantum Engine",
    tag: "Python",
    tagClass: "text-syntax-blue",
    icon: Cpu,
    description:
      "A multi-stage propulsion engine with procedurally generated internal pipe routing.",
  },
  {
    href: "#",
    title: "Bio-Dome Structure",
    tag: "Geo Nodes",
    tagClass: "text-syntax-green",
    icon: Dna,
    description:
      "Hexagonal lattice generation script for botanical containment on exoplanets.",
  },
  {
    href: "#",
    title: "Fractal Terrain",
    tag: "VEX",
    tagClass: "text-syntax-pink",
    icon: MountainSnow,
    description:
      "Noise-based displacement terrain generating realistic erosion and sediment flow.",
  },
] as const;

export function Gallery() {
  return (
    <section className="mx-auto max-w-7xl px-6 py-20 lg:px-8">
      <div className="mb-10 flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-end">
        <div>
          <h2 className="mb-2 text-2xl font-bold tracking-tight">
            Procedural Collection
          </h2>
          <p className="font-light text-secondary">
            Explore the gallery of generated 3D assets and their source code.
          </p>
        </div>
        <button
          type="button"
          className="group flex items-center gap-2 text-sm font-medium text-secondary transition-colors hover:text-accent"
        >
          View All Gallery{" "}
          <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
        </button>
      </div>

      <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        {cards.map(
          ({ href, title, tag, tagClass, icon: Icon, description }) => (
            <a
              key={title}
              href={href}
              className="group block overflow-hidden rounded-lg border border-[#27272a] bg-surface transition-all duration-300 hover:-translate-y-1 hover:border-[#3f3f46] hover:shadow-2xl hover:shadow-black/50"
            >
              <div className="relative flex h-52 items-center justify-center overflow-hidden border-b border-[#27272a] bg-[#121212]">
                <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-[#27272a] to-transparent opacity-40" />
                <Icon className="relative z-10 h-12 w-12 text-[#3f3f46] transition-colors duration-500 group-hover:scale-110 group-hover:text-secondary" />
              </div>
              <div className="p-6">
                <div className="mb-3 flex items-start justify-between">
                  <h3 className="font-semibold text-primary transition-colors group-hover:text-accent">
                    {title}
                  </h3>
                  <span
                    className={`rounded border border-[#27272a] bg-[#121212] px-2 py-1 font-mono text-[10px] ${tagClass}`}
                  >
                    {tag}
                  </span>
                </div>
                <p className="line-clamp-2 text-sm leading-relaxed text-secondary">
                  {description}
                </p>
              </div>
            </a>
          ),
        )}
      </div>
    </section>
  );
}
