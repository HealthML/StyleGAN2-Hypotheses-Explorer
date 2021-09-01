<script lang="ts">
  import ImageSelectorImage from "./ImageSelectorImage.svelte";

  export let images: string[] = [];

  let imagesAndUndefined: (string | undefined)[];
  $: imagesAndUndefined = [...images, undefined];
</script>

<div class="container">
  {#each imagesAndUndefined as image}
    <ImageSelectorImage
      {image}
      on:remove={() => (images = images.filter((_image) => image !== _image))}
      on:add={(image) => (images = [...new Set([...images, ...image.detail])])}
    />
  {/each}
</div>
<p>
  Generate images similar to the above
  <i>{images.length === 0 ? "(none selected)" : ""}</i>
</p>

<style>
  .container {
    display: flex;
    flex-wrap: wrap;
  }
</style>
