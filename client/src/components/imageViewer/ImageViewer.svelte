<script lang="ts">
  import type { SpriteMapPart } from "../../logic/stores/displayed";
  import LoadingIcon from "../loading/LoadingIcon.svelte";

  export let image: SpriteMapPart;
  export let style: string = "";
  export let classes: string = "";

  const IMAGE_SIZE = 256;

  let computed_style: string;
  $: computed_style = `
        width: ${IMAGE_SIZE}px;
        height: ${IMAGE_SIZE}px;
        background-size: auto ${IMAGE_SIZE}px;
        background-image: url(${image.src.url});
        background-position: -${
          (image.offsetX / image.height) * IMAGE_SIZE
        }px 0;
        ${style}
    `;
</script>

<div class={classes} style={computed_style} />
{#if image.loading}
  <div
    style="position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%); "
  >
    <LoadingIcon />
  </div>
{/if}
