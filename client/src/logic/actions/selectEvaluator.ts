// select evaluator
// -> generate all ratings new

import type { Evaluator } from "../../api";
import { displayedImages, displayedStyles } from "../stores/displayed";
import { activeEvaluator } from "../stores/evaluator";
import { Action } from "./action";

export class SelectEvaluatorAction extends Action<[Evaluator]> {
  protected async beforeCollect(evaluator: Evaluator) {
    activeEvaluator.set(evaluator);
  }

  protected async collectChangesResultView(): ReturnType<
    Action["collectChangesResultView"]
  > {
    const styles = displayedStyles.get();
    const images = displayedImages.get();
    if (!styles) {
      throw new Error("No styles shown");
    } else if (!images) {
      throw new Error("No images shown");
    } else {
      return {
        images: [],
        ratings: [styles.flat(), images].flat(),
      };
    }
  }

  protected async collectChangesStyleView(): ReturnType<
    Action["collectChangesStyleView"]
  > {
    return this.collectChangesResultView();
  }
}
