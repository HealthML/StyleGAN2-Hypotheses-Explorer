<script lang="ts">
  import type { Model } from "../../api";
  import type { Action } from "../../logic/actions/action";
  import type { Writable } from "../../logic/tools/customStore";
  import LoadingIcon from "../loading/LoadingIcon.svelte";

  export let models: Promise<Writable<Model[]>>;
  export let selectModelAction: Action<[Model]>;
  export let activeModel: Writable<Model | undefined>;
  export let modelType: string;

  let _models: Writable<Model[]> | undefined = undefined;
  let loading = 0;
  $: {
    models.then((models) => (_models = models));
  }
</script>

<div class="dropdown" style="margin-right: 5px;">
  <button
    class="btn btn-primary dropdown-toggle"
    data-toggle="dropdown"
    aria-expanded="false"
    type="button">
    {#if $activeModel}
      {($activeModel ?? { name: "None" }).name}
    {:else}
      Select
      {modelType}
      model
    {/if}
    {#if !_models || loading > 0}
      <LoadingIcon color="white" size="small" />
    {/if}
  </button>
  <div class="dropdown-menu" role="menu">
    {#if _models}
      {#each $_models as model}
        <button
          class="dropdown-item"
          role="presentation"
          on:click={() => {
            loading++;
            selectModelAction.execute(model).then(() => loading--);
          }}>
          {model.name}
        </button>
      {/each}
    {/if}
  </div>
</div>
