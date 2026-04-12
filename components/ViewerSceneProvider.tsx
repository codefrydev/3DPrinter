"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type Dispatch,
  type SetStateAction,
} from "react";
import {
  DEFAULT_VIEWER_SCENE,
  loadViewerSceneFromStorage,
  mergeViewerScene,
  saveViewerSceneToStorage,
  type ViewerSceneSettings,
} from "@/lib/viewerScene";

type ViewerSceneContextValue = {
  scene: ViewerSceneSettings;
  setScene: Dispatch<SetStateAction<ViewerSceneSettings>>;
  updateScene: (partial: Partial<ViewerSceneSettings>) => void;
};

const ViewerSceneContext = createContext<ViewerSceneContextValue | null>(null);

export function ViewerSceneProvider({ children }: { children: React.ReactNode }) {
  const [scene, setScene] = useState<ViewerSceneSettings>(DEFAULT_VIEWER_SCENE);
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    const stored = loadViewerSceneFromStorage();
    if (stored) setScene(stored);
    setHydrated(true);
  }, []);

  useEffect(() => {
    if (!hydrated) return;
    saveViewerSceneToStorage(scene);
  }, [scene, hydrated]);

  const updateScene = useCallback((partial: Partial<ViewerSceneSettings>) => {
    setScene((prev) => mergeViewerScene({ ...prev, ...partial }));
  }, []);

  const value = useMemo(
    () => ({ scene, setScene, updateScene }),
    [scene, updateScene],
  );

  return <ViewerSceneContext.Provider value={value}>{children}</ViewerSceneContext.Provider>;
}

export function useViewerScene(): ViewerSceneContextValue {
  const ctx = useContext(ViewerSceneContext);
  if (!ctx) {
    throw new Error("useViewerScene must be used within ViewerSceneProvider");
  }
  return ctx;
}
