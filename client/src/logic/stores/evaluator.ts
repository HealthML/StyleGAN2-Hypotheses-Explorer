import type { Evaluator } from "../../api";
import { Writable } from "../tools/customStore";

export const activeEvaluator = new Writable<Evaluator | undefined>(undefined);
