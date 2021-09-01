export function clamp(value: number, lower: number, upper: number) {
  return Math.min(Math.max(lower, value), upper);
}
