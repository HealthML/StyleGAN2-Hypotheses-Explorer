import { clamp } from "./clamp";

export function ratingColor(rating: number) {
  if (rating >= 0) {
    return `rgb(0, ${clamp(255 * rating, 0, 255)}, 0)`;
  } else {
    return `rgb(${clamp(-255 * rating, 0, 255)}, 0, 0)`;
  }
}
