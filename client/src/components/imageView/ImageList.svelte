<script lang="ts">
  import { flip } from "svelte/animate";
  import { SwitchImageAction } from "../../logic/actions/switchImage";
  import type { SpriteMapImage } from "../../logic/stores/displayed";
  import { displayedImages } from "../../logic/stores/displayed";
  import { selectedImage } from "../../logic/stores/selectedImage";
  import { BlobURLFake } from "../../logic/tools/blobURL";
  import { Writable } from "../../logic/tools/customStore";
  import { imageList, selectorHeight } from "../../logic/tools/exportImageList";
  import { formatRating } from "../../logic/tools/formatRating";
  import { ratingColor } from "../../logic/tools/ratingColor";
  import ImageViewer from "../imageViewer/ImageViewer.svelte";

  let _selectedImage: SpriteMapImage;
  $: _selectedImage = $selectedImage ?? {
    src: new BlobURLFake(),
    container: new Writable<undefined>(undefined),
    height: 256,
    width: 256,
    offsetX: 0,
    rating: 0,
    style: {
      generatorId: 0,
      style: {},
    },
  };

  let _imageList: HTMLDivElement | undefined = undefined;
  $: imageList.set(_imageList);
  let _selectorHeight: number = 0;
  $: selectorHeight.set(_selectorHeight);
</script>

<div style="position: relative; display: inline-block; ">
  <ImageViewer
    image={_selectedImage}
    style="margin-bottom: 1rem; max-width: 100%;"
  />
</div>

<p>
  Current rating:
  <b style="color: {ratingColor(_selectedImage.rating)}; ">
    {formatRating(_selectedImage.rating)}
  </b>
</p>
<h4 style="margin: 0;">Reference Images:</h4>
<div class="list-group list-group-horizontal" bind:this={_imageList}>
  {#each $displayedImages as image (image)}
    <button
      animate:flip={{ duration: 200 }}
      class="list-group-item list-group-item-action"
      style=" padding: 0; border-style: none; background-color: transparent;
      z-index:{$selectedImage === image ? 1 : 0}; outline: none;"
      on:click={() => {
        if ($selectedImage !== image) {
          new SwitchImageAction().execute(image);
        }
      }}
    >
      <p
        class="text-center"
        style="margin: 0; color: {ratingColor(image.rating || 0)}; "
      >
        {formatRating(image.rating)}
      </p>
      <div
        style="width: 100%; height: 2rem; background-color: {ratingColor(
          image.rating
        )}"
      />
      <div style="position: relative; ">
        <ImageViewer classes="img-fluid" {image} />
      </div>
      {#if _selectedImage === image}
        <p
          bind:clientHeight={_selectorHeight}
          data-selector="true"
          class="text-center"
          style="margin: 0; color: black; border-bottom: 5px solid black; "
        >
          selected
        </p>
      {:else}
        <p
          data-selector="true"
          class="text-center"
          style="margin: 0; color: lightgray; border-bottom: 5px solid
          lightgray; "
        >
          not selected
        </p>
      {/if}
    </button>
  {/each}
</div>
