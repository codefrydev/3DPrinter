import { CodePanel } from "@/components/CodePanel";
import { Gallery } from "@/components/Gallery";
import { getFeaturedModel, listModelsForGallery } from "@/modelcode/registry";

export default function Home() {
  const featured = getFeaturedModel();
  const galleryModels = listModelsForGallery();

  return (
    <main id="main-content">
      <CodePanel model={featured} />
      <Gallery models={galleryModels} />
    </main>
  );
}
