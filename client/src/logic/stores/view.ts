import { Writable } from "../tools/customStore";

export enum View {
  RESULT_VIEW = "Result View",
  STYLE_VIEW = "Style View",
}

export const view = new Writable<View>(View.STYLE_VIEW);
