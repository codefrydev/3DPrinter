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
    return { title: "Not found | ModelGen" };
  }
  return {
    title: `${model.title} | ModelGen`,
    description: model.description,
  };
}

export default async function ViewModelPage({ params }: PageProps) {
  const { id } = await params;
  const model = getModelById(id);
  if (!model) notFound();

  return (
    <main>
      <p className="border-b border-line bg-surface/40 px-6 py-3 text-center text-sm text-secondary lg:px-8">
        <Link
          href="/#gallery"
          className="font-medium text-primary underline-offset-4 transition-colors hover:text-accent hover:underline"
        >
          Back to gallery
        </Link>
      </p>
      <CodePanel model={model} />
    </main>
  );
}
