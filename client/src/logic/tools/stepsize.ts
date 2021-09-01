import { activeGenerator } from "../stores/generator";

export function stepSize() {
  const generator = activeGenerator.get();
  if (generator) {
    return generator.stepSize;
  } else {
    throw new Error("No generator selected.");
  }
}

export function roundToStepSize(ratio: number) {
  return Math.round(ratio / stepSize()) * stepSize();
}
