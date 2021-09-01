<script lang="ts">
  import { onMount } from "svelte";
  import type { Generator } from "../../api";
  import { SelectGeneratorAction } from "../../logic/actions/selectGenerator";
  import { activeGenerator } from "../../logic/stores/generator";
  import { getGenerators } from "../../logic/stores/models";
  import type { Writable } from "../../logic/tools/customStore";
  import ModelSelector from "./ModelSelector.svelte";

  let generators: Promise<Writable<Generator[]>> = new Promise((_) => {});
  onMount(() => {
    generators = getGenerators();
  });
</script>

<ModelSelector
  models={generators}
  selectModelAction={new SelectGeneratorAction()}
  activeModel={activeGenerator}
  modelType="a generator"
/>
