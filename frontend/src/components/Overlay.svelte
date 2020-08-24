<script lang="ts">
    import { sidebarOpen } from "../stores";
</script>

<div
    class="{$sidebarOpen ? 'block' : 'hidden'} fixed z-20 inset-0 bg-black opacity-50 transition-opacity lg:hidden"
    on:click={() => ($sidebarOpen = false)} />
