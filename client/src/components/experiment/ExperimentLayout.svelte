<script lang="ts">
  import { ChangeViewAction } from "../../logic/actions/changeView";
  import { ShuffleImagesAction } from "../../logic/actions/shuffleImages";
  import { activeGenerator } from "../../logic/stores/generator";
  import { view, View } from "../../logic/stores/view";
  import { exportImageList } from "../../logic/tools/exportImageList";
  import EvaluatorSelector from "../modelSelection/EvaluatorSelector.svelte";
  import GeneratorSelector from "../modelSelection/GeneratorSelector.svelte";
  import ShuffleStylesPopup from "../styleMatrix/ShuffleStylesPopup.svelte";

  let openShuffleStylesPopup: boolean = false;

  let isOfflineMode: boolean = true;

  $: {
    const generator = $activeGenerator;
    if (generator) {
      isOfflineMode = generator.offlineMode;
    } else {
      isOfflineMode = false;
    }
  }
</script>

<div style="width: 100vw; height: auto;">
  <div class="container-fluid" style="padding: 0;">
    <div class="row" style="margin: 0;">
      <div
        class="col d-flex flex-row justify-content-center align-items-center
        align-content-center flex-wrap"
      >
        <div style="margin: 1rem; box-shadow: 1px 1px 8px 0px;">
          <div class="card">
            <div class="card-body">
              <div
                class="d-flex justify-content-between align-items-start
                flex-nowrap"
              >
                <h3>Evaluation</h3>
                <div
                  class="d-flex justify-content-between align-items-start flex-nowrap"
                >
                  <button
                    class="btn btn-primary"
                    style="margin-right: 5px;"
                    type="button"
                    on:click={exportImageList}
                  >
                    <i class="fa fa-download" />
                  </button>
                  <GeneratorSelector />
                  <button
                    class="btn btn-dark"
                    type="button"
                    on:click={() => {
                      // TODO number selectable - or plus and minus?
                      new ShuffleImagesAction().execute(8);
                    }}
                  >
                    <i class="fa fa-random" style="margin-right: 0.3rem;" />
                    Shuffle generated images
                  </button>
                </div>
              </div>
              <h4>Selected Image: <br /></h4>
              <slot name="imageList" />
            </div>
          </div>
        </div>
        <div style="margin: 1rem; box-shadow: 1px 1px 8px 0px;">
          <div class="card">
            <div class="card-body">
              <div
                class="d-flex justify-content-between align-items-start
                flex-nowrap"
              >
                <div>
                  <h3 style="float:left;">Styles</h3>
                  <div
                    class="dropdown"
                    style="float: left; margin-left: 0.2rem;"
                  >
                    <button
                      class="btn btn-light dropdown-toggle"
                      data-toggle="dropdown"
                      aria-expanded="false"
                      type="button"
                      style="height: 2.4rem;"
                    >
                      <i class="fa fa-eye" style="margin-right: 0.3rem;" />
                      {$view}</button
                    >
                    <div class="dropdown-menu" role="menu">
                      {#each [...Object.values(View)] as _view}
                        <button
                          class="dropdown-item"
                          role="presentation"
                          on:click={() => {
                            new ChangeViewAction().execute(_view);
                          }}
                        >
                          {_view}
                        </button>
                      {/each}
                    </div>
                  </div>
                </div>
                <div
                  class="d-flex justify-content-between align-items-start flex-nowrap"
                >
                  <EvaluatorSelector />
                  {#if !isOfflineMode}
                    <button
                      class="btn btn-dark"
                      type="button"
                      on:click={() => (openShuffleStylesPopup = true)}
                    >
                      <i class="fa fa-random" style="margin-right: 0.3rem;" />
                      Shuffle styles
                    </button>
                  {/if}
                </div>
              </div>
              <slot name="styleImageList" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
<slot />

{#if openShuffleStylesPopup}
  <ShuffleStylesPopup bind:openShuffleStylesPopup />
{/if}
