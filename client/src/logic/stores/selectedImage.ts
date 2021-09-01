import { Writable } from "../tools/customStore";
import type { SpriteMapImage } from "./displayed";

export const selectedImage = new Writable<SpriteMapImage | undefined>(
  undefined
);
