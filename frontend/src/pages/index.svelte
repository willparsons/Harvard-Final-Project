<script lang="ts">
    import { metatags } from "@sveltech/routify";
    metatags.title = "Chat :)";
    metatags.description = "Index page";

    import Message, { generateMessage } from "../components/Message.svelte";

    const message1 = generateMessage(
        "MF DOOM",
        "https://cdn.shopify.com/s/files/1/0078/0225/7497/files/mf-doom-png-7_1200x630.png",
        "one beef left"
    );

    const message2 = generateMessage(
        "Jay Z",
        "https://i.pinimg.com/originals/1d/a8/8a/1da88a8e669e8d67fa0a50d53e503432.jpg",
        "bro i am a cossoint"
    );

    const messages = [message1, message2];
</script>

<!--Central section-->
<div class="page-content" data-simplebar>
    {#each messages as message}
        <Message {...message} />
    {/each}
</div>

<!--Message input field-->
<input
    class="bg-gray-900 focus:outline-none focus:shadow-outline border border-site-color-input py-2 px-4 block w-full
    appearance-none leading-normal"
    type="text"
    placeholder="Message..." />
