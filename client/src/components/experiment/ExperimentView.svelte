<script lang="ts">
    import ImageList from "../imageView/ImageList.svelte";

    import StyleMatrix from "../styleMatrix/StyleMatrix.svelte";
    import ExperimentLayout from "./ExperimentLayout.svelte";
</script>

<ExperimentLayout>
    <div slot="imageList">
        <ImageList />
    </div>
    <ul class="list-group list-group-horizontal" slot="styleImageList">
        <StyleMatrix />
    </ul>
</ExperimentLayout>
