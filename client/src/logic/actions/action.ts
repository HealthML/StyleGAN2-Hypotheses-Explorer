import { fetchImages, fetchRatings } from "../api";
import {
  displayedImages,
  RatedSpriteMapPart,
  SpriteMapPart,
} from "../stores/displayed";
import { selectedImage } from "../stores/selectedImage";
import { view, View } from "../stores/view";
import type { Writable } from "../tools/customStore";

export declare interface Changes {
  ratings: RatedSpriteMapPart[];
  images: RatedSpriteMapPart[];
}

export abstract class Action<ArgsTypes extends Array<any> = []> {
  protected abstract collectChangesResultView(
    ...args: ArgsTypes
  ): Promise<Changes>;
  protected abstract collectChangesStyleView(
    ...args: ArgsTypes
  ): Promise<Changes>;
  protected async beforeCollect(...args: ArgsTypes): Promise<void> {}

  private static actionQueue = Promise.resolve();

  private async collectChanges(...args: ArgsTypes) {
    switch (view.get()) {
      case View.RESULT_VIEW:
        return this.collectChangesResultView(...args);
      case View.STYLE_VIEW:
        return this.collectChangesStyleView(...args);
      default:
        throw new Error("");
    }
  }

  private async fetchChanges(
    changes: Changes
  ): Promise<[number[], SpriteMapPart[]]> {
    return Promise.all([
      fetchRatings(
        changes.ratings.map((ratedSpriteMapPart) => ratedSpriteMapPart.style)
      ).catch(() => changes.ratings.map((_) => 0)),
      fetchImages(
        changes.images.map((ratedSpriteMapPart) => ratedSpriteMapPart.style)
      ).catch(() =>
        changes.images.map((ratedSpriteMapPart) => ratedSpriteMapPart)
      ),
    ]);
  }

  private applyChanges(
    changes: Changes,
    ratings: number[],
    images: SpriteMapPart[]
  ): void {
    for (let index = 0; index < ratings.length; index++) {
      changes.ratings[index].rating = ratings[index];
      changes.ratings[index].loading = false;
    }
    for (let index = 0; index < images.length; index++) {
      changes.images[index].src.decreaseUses();
      Object.assign(changes.images[index], images[index]);
      changes.images[index].loading = false;
    }
  }

  private collectContainersToBeUpdated(changes: Changes) {
    const containersToBeUpdated = new Set<Writable<any>>();
    const _selectedImage = selectedImage.get();
    function addToContainersToBeUpdated(image: RatedSpriteMapPart) {
      if (_selectedImage === image) {
        containersToBeUpdated.add(selectedImage);
      }
      containersToBeUpdated.add(image.container);
    }
    changes.images.forEach(addToContainersToBeUpdated);
    changes.ratings.forEach(addToContainersToBeUpdated);

    return containersToBeUpdated;
  }

  private updateView(containersToBeUpdated: Set<Writable<any>>) {
    if (containersToBeUpdated.has(displayedImages)) {
      displayedImages.set(
        displayedImages.get()!.sort((i1, i2) => i1.rating - i2.rating)
      );
    }
    for (const container of containersToBeUpdated.values()) {
      container.set(container.get());
    }
  }

  private setImagesToLoading(changes: Changes) {
    changes.images.forEach((image) => (image.loading = true));
    changes.ratings.forEach((image) => (image.loading = true));
  }

  public async execute(...args: ArgsTypes): Promise<void> {
    Action.actionQueue = Action.actionQueue.then(async () => {
      await this.beforeCollect(...args);
      const changes = await this.collectChanges(...args);
      const containersToBeUpdated = this.collectContainersToBeUpdated(changes);
      this.setImagesToLoading(changes);
      this.updateView(containersToBeUpdated);
      const [ratings, images] = await this.fetchChanges(changes);
      this.applyChanges(changes, ratings, images);
      this.updateView(containersToBeUpdated);
    });
    await Action.actionQueue;
  }
}
