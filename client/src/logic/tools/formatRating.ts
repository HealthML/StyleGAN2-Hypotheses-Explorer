export function formatRating(rating: number): string {
  return parseFloat(rating.toFixed(3)).toString();
}
