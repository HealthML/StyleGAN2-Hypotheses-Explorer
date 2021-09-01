<script lang="ts">
  import EvaluatorSelector from "./EvaluatorSelector.svelte";
  import GeneratorSelector from "./GeneratorSelector.svelte";
</script>

<div
  class="d-flex flex-row justify-content-center align-items-center
    align-content-center align-self-center"
  style="width: 100vw; height: 100vh;"
>
  <div
    class="container d-flex flex-column justify-content-start align-items-start
      align-content-start align-self-start m-auto"
  >
    <h1 style="padding-bottom: 1rem; ">Select models</h1>
    <GeneratorSelector />
    <div style="padding: 0.5rem; width: 0; height: 0;" />
    <EvaluatorSelector />
  </div>
</div>
