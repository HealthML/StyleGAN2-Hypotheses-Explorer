<script lang="ts">
  import { ShuffleStylesAction } from "../../logic/actions/shuffleStyles";
  import { activeEvaluator } from "../../logic/stores/evaluator";
  import { activeGenerator } from "../../logic/stores/generator";
  import ImageSelector from "./ImageSelector.svelte";

  export let openShuffleStylesPopup: boolean = true;

  let numGenStylesPerLayer: number | undefined;
  let reduceNumberOfLayersBy: number | undefined;
  let useSameStylesForAllLayers: boolean | undefined;
  let optimizeStyles: boolean | undefined;
  let numberOfLayers: number | undefined;
  let stylesFromImages: string[] = [];

  function updateValuesFromGenerator(_: any) {
    const _activeEvaluator = $activeEvaluator ?? { id: -1 };
    const _activeGenerator = $activeGenerator ?? {
      settings: {
        numGenStylesPerLayer: undefined,
        reduceNumberOfLayersBy: undefined,
        useSameStylesForAllLayers: undefined,
        optimizeStyles: undefined,
        stylesFromImages: undefined,
      },
      numberOfLayers: undefined,
    };
    numGenStylesPerLayer = _activeGenerator.settings.numGenStylesPerLayer;
    reduceNumberOfLayersBy = _activeGenerator.settings.reduceNumberOfLayersBy;
    useSameStylesForAllLayers =
      _activeGenerator.settings.useSameStylesForAllLayers;
    optimizeStyles =
      _activeGenerator.settings.optimizeStyles === _activeEvaluator.id;
    stylesFromImages = _activeGenerator.settings.stylesFromImages ?? [];
    numberOfLayers = _activeGenerator.numberOfLayers;
  }
  $: updateValuesFromGenerator($activeGenerator);

  function confirm() {
    const _activeEvaluator = $activeEvaluator ?? { id: undefined };
    new ShuffleStylesAction().execute({
      numGenStylesPerLayer: numGenStylesPerLayer || 8,
      reduceNumberOfLayersBy: reduceNumberOfLayersBy || 0,
      useSameStylesForAllLayers: useSameStylesForAllLayers || false,
      optimizeStyles: optimizeStyles ? _activeEvaluator.id : undefined,
      stylesFromImages:
        stylesFromImages.length > 0 ? stylesFromImages : undefined,
    });
    openShuffleStylesPopup = false;
  }
  function cancel() {
    openShuffleStylesPopup = false;
  }
</script>

<div
  class="d-flex flex-row justify-content-center align-items-center align-content-center align-self-center settings-popup"
>
  <div
    class="container d-flex flex-column justify-content-start align-items-start align-content-start align-self-start m-auto"
  >
    <h1>Settings</h1>

    <div style="padding: 0.5rem;width: 0;height: 0;" />
    <input
      class="border rounded"
      type="number"
      min={1}
      max={15}
      step={1}
      bind:value={numGenStylesPerLayer}
    />
    <p>Number of styles per layer</p>

    <div style="padding: 0.5rem;width: 0;height: 0;" />
    <input
      class="border rounded"
      type="number"
      min={0}
      max={(numberOfLayers ?? 1) - 1}
      step={1}
      bind:value={reduceNumberOfLayersBy}
    />
    <p>Reduce number of layers by</p>

    <div style="padding: 0.5rem;width: 0;height: 0;" />
    <div class="dropdown">
      <button
        class="btn btn-primary dropdown-toggle"
        data-toggle="dropdown"
        aria-expanded="false"
        type="button">Use same style for all layers</button
      >
      <div class="dropdown-menu" role="menu">
        <button
          class="dropdown-item"
          role="presentation"
          on:click={() => (useSameStylesForAllLayers = true)}
        >
          Yes
        </button>
        <button
          class="dropdown-item"
          role="presentation"
          on:click={() => (useSameStylesForAllLayers = false)}
        >
          No
        </button>
      </div>
    </div>
    <p>
      Selected:
      <strong
        >{useSameStylesForAllLayers === true
          ? "Yes"
          : useSameStylesForAllLayers === false
          ? "No"
          : ""}</strong
      >
    </p>

    <div style="padding: 0.5rem;width: 0;height: 0;" />
    <ImageSelector bind:images={stylesFromImages} />

    <div style="padding: 0.5rem;width: 0;height: 0;" />
    <div class="dropdown">
      <button
        class="btn btn-primary dropdown-toggle"
        data-toggle="dropdown"
        aria-expanded="false"
        type="button">Optimize generated styles</button
      >
      <div class="dropdown-menu" role="menu">
        <button
          class="dropdown-item"
          role="presentation"
          on:click={() => (optimizeStyles = true)}
        >
          Yes
        </button>
        <button
          class="dropdown-item"
          role="presentation"
          on:click={() => (optimizeStyles = false)}
        >
          No
        </button>
      </div>
    </div>
    <p>
      Selected:
      <strong
        >{optimizeStyles === true
          ? "Yes"
          : optimizeStyles === false
          ? "No"
          : ""}</strong
      >
    </p>

    <div style="padding: 0.5rem;width: 0;height: 0;" />
    <div style="width: 100%;">
      <button class="btn btn-danger" type="button" on:click={cancel}>
        Cancel
        <i class="fa fa-close d-inline" style="margin-left: 0.5rem;" />
      </button>
      <button
        class="btn btn-success text-center float-right"
        type="button"
        on:click={confirm}
      >
        Confirm
        <i class="fa fa-check d-inline" style="margin-left: 0.5rem;" />
      </button>
    </div>
  </div>
</div>

<style>
  .settings-popup {
    width: auto;
    max-width: 100vw;
    min-width: 50vw;
    height: auto;
    position: fixed;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    background-color: white;
    z-index: 2;
    box-shadow: 1px 1px 8px 0px;
    padding: 1rem;
  }
</style>
