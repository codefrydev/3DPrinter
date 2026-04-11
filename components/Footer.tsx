export function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="mt-auto border-t border-line bg-bg">
      <div className="mx-auto flex max-w-7xl flex-col gap-8 px-6 py-12 sm:flex-row sm:items-center sm:justify-between lg:px-8">
        <div>
          <p className="text-sm font-semibold tracking-tight text-primary">
            ModelGen
          </p>
          <p className="mt-1 max-w-sm text-sm leading-relaxed text-secondary">
            Procedural 3D showcases and generation scripts.
          </p>
        </div>
        <nav
          className="flex flex-wrap gap-x-8 gap-y-3 text-sm font-medium text-secondary"
          aria-label="Footer"
        >
          <a
            href="#showcase"
            className="transition-colors hover:text-primary motion-reduce:transition-none"
          >
            Showcase
          </a>
          <a
            href="#gallery"
            className="transition-colors hover:text-primary motion-reduce:transition-none"
          >
            Gallery
          </a>
          <a
            href="#"
            className="transition-colors hover:text-primary motion-reduce:transition-none"
          >
            Documentation
          </a>
        </nav>
        <p className="text-xs text-secondary sm:text-right">
          © {year} ModelGen. All rights reserved.
        </p>
      </div>
    </footer>
  );
}
