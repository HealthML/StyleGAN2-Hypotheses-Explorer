export function lerp(a: number, b: number, x: number) {
  return a * x + b * (1 - x);
}
