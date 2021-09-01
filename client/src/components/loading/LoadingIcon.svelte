<script lang="ts">
  export let color = "black";
  export let size = "large";
</script>

<span
  class="spinner-border {size === 'small' ? 'spinner-border-sm' : ''}"
  role="status"
  style="border-width: 11%; border-style: solid; color: {color};" />
