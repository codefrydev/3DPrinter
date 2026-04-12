import Link from "next/link";

const footerLinkClass =
  "transition-colors hover:text-primary motion-reduce:transition-none";

export function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="mt-auto border-t border-line bg-bg">
      <div className="mx-auto grid max-w-7xl grid-cols-1 gap-8 px-6 py-12 sm:grid-cols-[minmax(0,1fr)_auto_minmax(0,1fr)] sm:items-center sm:gap-6 lg:gap-8 lg:px-8">
        <div className="min-w-0">
          <p className="text-sm font-semibold tracking-tight text-primary">
            <Link href="/" className="transition-colors hover:text-accent motion-reduce:transition-none">
              3D Printer
            </Link>
          </p>
          <p className="mt-1 max-w-sm text-sm leading-relaxed text-secondary">
            Procedural 3D showcases and generation scripts.
          </p>
        </div>

        <nav aria-label="Footer" className="flex justify-center sm:justify-center">
          <ul className="flex list-none flex-wrap items-center justify-center gap-x-8 gap-y-3 text-sm font-medium text-secondary">
            <li>
              <Link href="/#showcase" className={footerLinkClass}>
                Showcase
              </Link>
            </li>
            <li>
              <Link href="/#gallery" className={footerLinkClass}>
                Gallery
              </Link>
            </li>
            <li>
              <Link href="/docs/" className={footerLinkClass}>
                Documentation
              </Link>
            </li>
          </ul>
        </nav>

        <p className="text-xs text-secondary sm:justify-self-end sm:text-right">
          © {year} Codefrydev. All rights reserved.
        </p>
      </div>
    </footer>
  );
}
