import { CodePanel } from "@/components/CodePanel";
import { Gallery } from "@/components/Gallery";
import { Header } from "@/components/Header";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col">
      <Header />
      <main className="flex-1">
        <CodePanel />
        <Gallery />
      </main>
    </div>
  );
}
