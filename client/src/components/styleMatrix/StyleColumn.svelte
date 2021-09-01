<script lang="ts">
  import { flip } from "svelte/animate";
  import { ChangeImageStyleAction } from "../../logic/actions/changeImageStyle";
  import type {
    SpriteMapImage,
    SpriteMapStyle,
  } from "../../logic/stores/displayed";
  import { selectedImage } from "../../logic/stores/selectedImage";
  import { clamp } from "../../logic/tools/clamp";
  import { lerp } from "../../logic/tools/lerp";
  import { ratingColor } from "../../logic/tools/ratingColor";
  import { roundToStepSize } from "../../logic/tools/stepsize";
  import type { StyleArrayElement } from "../../logic/tools/styleArrayElement";
  import { stylesEqual } from "../../logic/tools/styleArrayElement";
  import ImageViewer from "../imageViewer/ImageViewer.svelte";

  export let layer: number;

  export let layerStyles: SpriteMapStyle[];
  let _selectedImage: SpriteMapImage | undefined;
  $: _selectedImage = $selectedImage;
  let _selectedStyle: StyleArrayElement | undefined = undefined;
  $: updateSelectedStyle(_selectedImage);

  let draggedStyleIndex: undefined | number = undefined;
  let container: HTMLUListElement;
  let draggerHeight: number;
  let startingOffset = 0;
  let relPosition = 0;
  $: updateRelPosition(_selectedStyle, layerStyles, draggedStyleIndex);
  let draggerYCSS = "0";
  $: updateDraggerYCSS(container, relPosition);

  function updateSelectedStyle(..._: any) {
    if (_selectedImage && _selectedImage.style.style.styleArray) {
      _selectedStyle = _selectedImage.style.style.styleArray[layer];
    } else {
      _selectedStyle = undefined;
    }
  }

  function updateRelPosition(..._: any) {
    if (_selectedStyle && draggedStyleIndex === undefined) {
      relPosition = relPositionFromFloatStyleIndex(
        floatStyleIndexFromStyle(_selectedStyle)
      );
    }
  }

  function updateDraggerYCSS(..._: any) {
    if (container) {
      const rect = container.getBoundingClientRect();
      draggerYCSS = `calc(${relPosition} * (100% - ${rect.width}px))`;
    }
  }

  function getSelectedStyle() {
    if (_selectedStyle) {
      return _selectedStyle;
    } else {
      throw new Error("No image selected");
    }
  }

  function changeStyle(floatStyleIndex: number) {
    const selectedStyle = getSelectedStyle();
    const newStyle = styleFromFloatStyleIndex(floatStyleIndex);
    if (!stylesEqual(selectedStyle, newStyle)) {
      selectedStyle.proportionStyle1 = newStyle.proportionStyle1;
      selectedStyle.style1 = newStyle.style1;
      selectedStyle.style2 = newStyle.style2;
      new ChangeImageStyleAction().execute(layer);
    }
  }

  function styleFromFloatStyleIndex(
    floatStyleIndex: number
  ): NonNullable<typeof _selectedStyle> {
    const lower = Math.floor(floatStyleIndex);
    const upper = Math.ceil(floatStyleIndex);
    const proportionUpper = floatStyleIndex - lower;
    return {
      style1: layerStyles[upper].id,
      style2: layerStyles[lower].id,
      proportionStyle1: proportionUpper,
    };
  }

  function floatStyleIndexFromStyle(
    style: NonNullable<typeof _selectedStyle>
  ): number {
    let style1Index = layerStyles.findIndex(
      (_style) => _style.id === style.style1
    );
    let style2Index = layerStyles.findIndex(
      (_style) => _style.id === style.style2
    );
    if (style1Index === -1 && style2Index === -1) {
      // The image has an invalid style. This only happens briefly when the selected image changes before the layerStyles are updated
      return 0;
    } else {
      if (style1Index === -1) {
        style1Index = style2Index;
      }
      if (style2Index === -1) {
        style2Index = style1Index;
      }
      const proportion = style.proportionStyle1 ?? 1;
      return lerp(style1Index, style2Index, proportion);
    }
  }

  function floatStyleIndexFromRelPosition(relPosition: number) {
    return relPosition * (layerStyles.length - 1);
  }

  function relPositionFromFloatStyleIndex(floatStyleIndex: number) {
    return floatStyleIndex / (layerStyles.length - 1);
  }

  let draggingDragger = false;
  function getRelPositionNoStartingOffset(e: MouseEvent) {
    const containerRect = container.getBoundingClientRect();
    const relPositionTop = containerRect.top + draggerHeight / 2;
    const relPositionBottom = containerRect.bottom - draggerHeight / 2;
    return (
      1 - (e.clientY - relPositionBottom) / (relPositionTop - relPositionBottom)
    );
  }
  function roundRelPositionToStepSize(relPosition: number) {
    return relPositionFromFloatStyleIndex(
      roundToStepSize(floatStyleIndexFromRelPosition(relPosition))
    );
  }
  function dragDragger(e: MouseEvent) {
    relPosition = clamp(
      roundRelPositionToStepSize(
        getRelPositionNoStartingOffset(e) - startingOffset
      ),
      0,
      1
    );
  }
  function startDraggingDragger(e: MouseEvent) {
    draggingDragger = true;
    const _relPosition = getRelPositionNoStartingOffset(e);
    startingOffset = _relPosition - relPosition;
  }
  function stopDraggingDragger(e: MouseEvent) {
    dragDragger(e);
    draggingDragger = false;
  }

  function dragStyle(e: MouseEvent) {
    const containerRect = container.getBoundingClientRect();
    const containerTop = containerRect.top;
    const containerBottom = containerRect.bottom;
    const _relPosition = clamp(
      1 - (e.clientY - containerBottom) / (containerTop - containerBottom),
      0,
      1
    );
    const newStyleIndex = Math.round(
      floatStyleIndexFromRelPosition(_relPosition)
    );
    if (newStyleIndex !== draggedStyleIndex!) {
      const newStyle = layerStyles[newStyleIndex];
      layerStyles[newStyleIndex] = layerStyles[draggedStyleIndex!];
      layerStyles[draggedStyleIndex!] = newStyle;
      draggedStyleIndex = newStyleIndex;
      // Trigger local UI update
      layerStyles = layerStyles;
    }
  }
  function startDraggingStyle(e: MouseEvent, styleIndex: number) {
    draggedStyleIndex = styleIndex;
    dragStyle(e);
  }
  function stopDraggingStyle(e: MouseEvent) {
    dragStyle(e);
    draggedStyleIndex = undefined;
  }

  function drag(e: MouseEvent) {
    if (draggingDragger) {
      dragDragger(e);
    }
    if (draggedStyleIndex !== undefined) {
      dragStyle(e);
    }
  }
  function stopDragging(e: MouseEvent) {
    let changes = false;
    if (draggingDragger) {
      stopDraggingDragger(e);
      changes = true;
    }
    if (draggedStyleIndex !== undefined) {
      stopDraggingStyle(e);
      changes = true;
    }
    if (changes) {
      changeStyle(floatStyleIndexFromRelPosition(relPosition));
    }
  }
</script>

<svelte:body
  on:mouseup={stopDragging}
  on:mouseleave={stopDragging}
  on:mousemove={drag} />

<ul
  bind:this={container}
  class="list-group"
  style="border-style: none; position: relative; "
>
  {#each layerStyles as style, styleIndex (style.id)}
    <li
      class="list-group-item"
      style="padding: 0; border-style: none; cursor: grab;"
      animate:flip={{ duration: 400 }}
      on:mousedown|preventDefault={(e) => startDraggingStyle(e, styleIndex)}
    >
      <ImageViewer classes="img-fluid" image={style} />
      <div
        class="rating"
        style="background-color: {ratingColor(style.rating)}"
      />
    </li>
  {/each}
  <div
    bind:clientHeight={draggerHeight}
    class="dragger"
    style="top: {draggerYCSS}; left: 0; padding-top: 100%; position: absolute; cursor: grab; "
    on:mousedown|preventDefault={startDraggingDragger}
  />
</ul>

<style>
  .dragger:hover {
    border: 6px solid black;
    width: calc(100% + 12px);
    transform: translate(-6px, -6px);
  }
  .dragger {
    background-color: rgba(0, 0, 0, 0.4);
    border: 4px solid black;
    width: calc(100% + 8px);
    transition: border 0.15s ease-in-out, transform 0.15s ease-in-out,
      width 0.15s ease-in-out;
    transform: translate(-4px, -4px);
    border-radius: 4%;
  }
  .rating {
    position: absolute;
    right: 0;
    top: 0;
    bottom: 0;
    width: 1rem;
  }
</style>
