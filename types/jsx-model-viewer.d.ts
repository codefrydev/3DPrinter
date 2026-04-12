import type { DetailedHTMLProps, HTMLAttributes } from "react";

declare module "react" {
  namespace JSX {
    interface IntrinsicElements {
      "model-viewer": DetailedHTMLProps<
        HTMLAttributes<HTMLElement> & {
          src?: string;
          alt?: string;
          loading?: "auto" | "lazy";
          "camera-controls"?: boolean | string;
          "auto-rotate"?: boolean | string;
          "environment-image"?: string;
          exposure?: string | number;
          "shadow-intensity"?: string;
          "shadow-softness"?: string;
          "interaction-prompt"?: "auto" | "none" | string;
        },
        HTMLElement
      >;
    }
  }
}

export {};
