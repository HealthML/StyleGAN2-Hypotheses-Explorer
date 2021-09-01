<script lang="ts">
  import { onMount } from "svelte";
  import ExperimentView from "../components/experiment/ExperimentView.svelte";
  import ModelSelectorView from "../components/modelSelection/ModelSelectorView.svelte";
  import { activeEvaluator } from "../logic/stores/evaluator";
  import { activeGenerator } from "../logic/stores/generator";

  let mounted = false;
  onMount(() => {
    mounted = true;
  });
</script>

{#if mounted}
  {#if !$activeEvaluator || !$activeGenerator}
    <ModelSelectorView />
  {:else}
    <ExperimentView />
  {/if}
{/if}
