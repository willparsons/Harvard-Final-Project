<script lang="ts">
    import { sidebarOpen } from "../stores";
    import Link from "./Link.svelte";
</script>

<div
    class="{$sidebarOpen ? 'translate-x-0 ease-out' : '-translate-x-full ease-in'} fixed z-30 inset-y-0 left-0 w-64
    transition duration-300 transform bg-site-color border-r border-site-color overflow-y-auto lg:translate-x-0
    lg:static lg:inset-0">

    <!--Logo and text-->
    <div class="flex items-center justify-center h-20 pt-8">
        <div class="flex items-center">
            <i class="fab fa-discord fa-3x" />
            <span class="text-white text-2xl mx-2 font-semibold">Chat</span>
        </div>
    </div>

    <!--Sidebar Links-->
    <nav class="mt-10">
        <Link link={'/index'} iconClass={'fas fa-comments'} text={'Chat'} />
        <Link link={'friends'} iconClass={'fas fa-user-friends'} text={'Friends'} />
        <Link link={'login'} iconClass={'fas fa-comments'} text={'Login'} />
    </nav>
</div>
