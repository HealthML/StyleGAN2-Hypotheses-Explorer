import type { Style } from "../../api";
import type { BlobURLFake } from "../tools/blobURL";
import { Writable } from "../tools/customStore";

export declare interface SpriteMapPart {
  src: BlobURLFake;
  width: number;
  height: number;
  offsetX: number;
  loading?: boolean;
}

export declare interface RatedSpriteMapPart extends SpriteMapPart {
  rating: number;
  style: Style;
  container: Writable<any>;
}

export declare interface SpriteMapStyle extends RatedSpriteMapPart {
  id: number;
}

export declare interface SpriteMapImage extends RatedSpriteMapPart {}

export const displayedStyles = new Writable<SpriteMapStyle[][]>([]);

export const displayedImages = new Writable<SpriteMapImage[]>([]);
