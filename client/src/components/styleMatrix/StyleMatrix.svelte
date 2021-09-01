<script lang="ts">
  import type { SpriteMapStyle } from "../../logic/stores/displayed";
  import { displayedStyles } from "../../logic/stores/displayed";
  import StyleColumn from "./StyleColumn.svelte";

  let _displayedStyles: SpriteMapStyle[][];
  $: _displayedStyles = $displayedStyles;
</script>

{#each _displayedStyles as layerStyles, layer (layer)}
  <li class="list-group-item" style="background-color: transparent; ">
    <p class="text-center" style="margin-bottom: 0.1rem;">Layer {layer}</p>
    <StyleColumn {layer} {layerStyles} />
  </li>
{/each}
