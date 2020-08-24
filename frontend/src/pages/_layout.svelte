<script lang="ts">
    import Overlay from "../components/Overlay.svelte";
    import Sidebar from "../components/Sidebar.svelte";
    import Navbar from "../components/Navbar.svelte";
</script>

<div class="flex h-full">
    <Overlay />

    <Sidebar />

    <div class="flex flex-col flex-1 overflow-hidden">
        <Navbar />

        <main class="flex flex-col h-full overflow-hidden">
            <slot>No content given.</slot>
        </main>
    </div>
</div>
