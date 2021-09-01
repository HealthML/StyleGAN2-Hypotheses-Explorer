<script lang="ts">
  import { fromEvent } from "file-selector";
  import { createEventDispatcher } from "svelte";
  import { blobToBase64 } from "../../logic/tools/blobToBase64";
  import LoadingIcon from "../loading/LoadingIcon.svelte";

  const dispatch = createEventDispatcher();

  export let image: string | undefined;

  let working = false;

  function selectImage() {
    const fileInput = document.createElement("input");
    fileInput.style.display = "none";
    fileInput.type = "file";
    fileInput.name = "Create styles similar to...";
    fileInput.accept = "image/*";
    fileInput.multiple = true;
    document.body.appendChild(fileInput);
    fileInput.onchange = (e) => {
      working = true;
      fromEvent(e)
        .then((files) =>
          files.map((file) => ("getAsFile" in file ? file.getAsFile() : file))
        )
        .then((files) => files.filter((file) => file) as File[])
        .then((files) => Promise.all(files.map((file) => blobToBase64(file))))
        .then((files) => {
          dispatch("add", files);
        })
        .finally(() => {
          working = false;
        });
      document.body.removeChild(fileInput);
    };
    fileInput.click();
  }
</script>

<div
  style={`
      ${image ? "background-image: url(data:image/*;base64," + image : ""}
`}
  on:click={() => {
    if (!working) {
      if (image) {
        dispatch("remove");
      } else {
        selectImage();
      }
    }
  }}
>
  {#if working}
    <LoadingIcon />
  {:else}
    <i
      class="fa fa-2x {image ? 'fa-trash redOnHover' : 'fa-plus greenOnHover'}"
    />
  {/if}
</div>

<style>
  :root {
    --size: 100px;
  }

  div {
    position: relative;
    width: var(--size);
    height: var(--size);
    background-size: contain;
    background-color: transparent;
    background-repeat: no-repeat;
    background-position: center center;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  i {
    cursor: pointer;
    width: var(--size);
    height: var(--size);
    text-align: center;
    vertical-align: middle;
    line-height: var(--size);
  }

  .redOnHover {
    opacity: 0;
  }
  .redOnHover:hover {
    opacity: 1;
    background-color: rgba(255, 0, 0, 0.6);
  }

  .greenOnHover:hover {
    background-color: rgba(0, 255, 0, 0.6);
  }
</style>
