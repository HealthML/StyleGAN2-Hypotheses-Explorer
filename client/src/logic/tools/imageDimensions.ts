export function getImageDimensions(imageUrl: string) {
  return new Promise<{ width: number; height: number }>((resolve, reject) => {
    const img = new Image();
    img.onload = () => {
      resolve({ width: img.width, height: img.height });
    };
    img.onerror = (e: any) => {
      reject(e);
    };
    img.src = imageUrl;
  });
}
