export function randint(min_inclusive: number, max_exclusive: number) {
  return Math.min(
    Math.floor(Math.random() * (max_exclusive - min_inclusive) + min_inclusive),
    max_exclusive - 1
  );
}
