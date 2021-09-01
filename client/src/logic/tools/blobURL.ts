export class BlobURLFake {
  readonly url: string =
    'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg"/>';
  increaseUses(_: number = 1) {}
  decreaseUses(_: number = 1) {}
}

export class BlobURL extends BlobURLFake {
  readonly url: string;

  constructor(blob: Blob, private uses = 0) {
    super();
    this.url = URL.createObjectURL(blob);
  }

  increaseUses(amount: number = 1) {
    this.uses += amount;
  }
  decreaseUses(amount: number = 1) {
    this.uses -= amount;
    if (this.uses <= 0) {
      URL.revokeObjectURL(this.url);
    }
  }
}

export function createBlobURL(blob: Blob) {
  return new BlobURL(blob);
}
