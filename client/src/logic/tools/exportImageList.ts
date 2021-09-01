import domtoimage from "dom-to-image";
import { saveAs } from "file-saver";
import { Writable } from "./customStore";

export let imageList = new Writable<HTMLDivElement | undefined>(undefined);
export let selectorHeight = new Writable<number>(0);

export async function exportImageList() {
  const _imageList = imageList.get();
  if (_imageList) {
    const blob = await domtoimage.toBlob(_imageList, {
      bgcolor: "white",
      filter: (node) =>
        node instanceof Element ? !node.hasAttribute("data-selector") : true,
      height: _imageList.clientHeight - selectorHeight.get(),
    });
    saveAs(blob, "ratings.png");
  }
}
