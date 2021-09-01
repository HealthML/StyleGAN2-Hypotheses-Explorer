<script lang="ts">
  import { onMount } from "svelte";
  import type { Evaluator } from "../../api";
  import { SelectEvaluatorAction } from "../../logic/actions/selectEvaluator";
  import { activeEvaluator } from "../../logic/stores/evaluator";
  import { getEvaluators } from "../../logic/stores/models";
  import type { Writable } from "../../logic/tools/customStore";
  import ModelSelector from "./ModelSelector.svelte";

  let evaluators: Promise<Writable<Evaluator[]>> = new Promise((_) => {});
  onMount(() => {
    evaluators = getEvaluators();
  });
</script>

<ModelSelector
  models={evaluators}
  selectModelAction={new SelectEvaluatorAction()}
  activeModel={activeEvaluator}
  modelType="an evaluator"
/>
