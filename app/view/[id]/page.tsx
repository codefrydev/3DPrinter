import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { CodePanel } from "@/components/CodePanel";
import {
  getModelById,
  MODEL_IDS,
} from "@/modelcode/registry";

type PageProps = {
  params: Promise<{ id: string }>;
};

export function generateStaticParams() {
  return MODEL_IDS.map((id) => ({ id }));
}

export async function generateMetadata({
  params,
}: PageProps): Promise<Metadata> {
  const { id } = await params;
  const model = getModelById(id);
  if (!model) {
    return { title: "Not found" };
  }
  return {
    title: model.title,
    description: model.description,
    openGraph: {
      title: model.title,
      description: model.description,
    },
    twitter: {
      title: model.title,
      description: model.description,
    },
  };
}

export default async function ViewModelPage({ params }: PageProps) {
  const { id } = await params;
  const model = getModelById(id);
  if (!model) notFound();

  return (
    <main id="main-content">
      <div className="border-b border-line bg-surface/40 px-6 py-3 text-center text-sm text-secondary lg:px-8">
        <div className="mx-auto flex max-w-7xl flex-col items-center gap-2 sm:flex-row sm:flex-wrap sm:justify-center sm:gap-x-6 sm:gap-y-1">
          <span className="flex flex-wrap items-center justify-center gap-x-4 gap-y-1">
            <Link
              href="/"
              className="font-medium text-primary underline-offset-4 transition-colors hover:text-accent hover:underline"
            >
              Home
            </Link>
            <Link
              href="/#gallery"
              className="font-medium text-primary underline-offset-4 transition-colors hover:text-accent hover:underline"
            >
              Back to gallery
            </Link>
          </span>
          <span className="font-medium text-primary sm:max-w-[min(100%,28rem)] sm:truncate">
            {model.title}
          </span>
        </div>
      </div>
      <CodePanel model={model} />
    </main>
  );
}
