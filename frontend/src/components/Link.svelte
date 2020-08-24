<script lang="ts">
    import { url, isActive } from "@sveltech/routify";

    export let link: string;

    export let iconClass: string = "fas fa-bug";
    export let text: string = "undefined";

    export let hasNotifications: boolean = false;
</script>

<a
    href={$url(link)}
    class="flex h-10 items-center mt-4 py-2 px-6 border-l-4 cursor-pointer {$isActive(link) ? 'sidebar-active-item' : 'sidebar-inactive-item'}">
    <i class={iconClass} />
    <span class="mx-4">{text}</span>

    {#if hasNotifications}
        <span class="relative inline-flex rounded-full h-3 w-3 bg-pink-500" />
    {/if}
</a>
