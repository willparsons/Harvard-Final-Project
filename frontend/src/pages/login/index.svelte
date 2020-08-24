<script lang="ts">
    import { metatags } from "@sveltech/routify";
    metatags.title = "Login";
    metatags.description = "Users can login here :)";

    export let isLoggedIn = false;

    let username = "";
    let password = "";

    function login() {
        console.log(username);
        console.log(password);
    }

    function handleKeyDown(e: KeyboardEvent) {
        if (e.keyCode === 13) login();
    }
</script>

<!-- routify:options name="login" -->

<div class="flex h-screen text-black">
    <div class="m-auto">
        {#if !isLoggedIn}
            <div class="w-full">
                <form class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">

                    <!--Username-->
                    <div class="mb-4">
                        <label class="form-label" for="username">Username</label>
                        <input
                            class="form-input leading-tight"
                            name="username"
                            type="text"
                            placeholder="Username"
                            bind:value={username}
                            on:keydown={handleKeyDown} />
                    </div>

                    <!--Password-->
                    <div class="mb-6">
                        <label class="form-label" for="password">Password</label>
                        <input
                            class="form-input leading-tight"
                            name="password"
                            id="password"
                            type="password"
                            placeholder="******************"
                            bind:value={password}
                            on:keydown={handleKeyDown} />
                        <p class="text-red-500 text-xs italic hidden" id="password-error">Please choose a password.</p>
                    </div>

                    <!--Submit / Forgot password-->
                    <div class="flex items-center justify-between">
                        <button
                            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded
                            focus:outline-none focus:shadow-outline"
                            type="button"
                            on:click={login}>
                            Sign In
                        </button>
                        <a
                            class="inline-block align-baseline font-bold text-sm text-blue-500 hover:text-blue-800"
                            href="#">
                            Forgot Password?
                        </a>
                    </div>
                </form>
            </div>
        {:else}
            <button type="button">Logout</button>
        {/if}
    </div>
</div>
