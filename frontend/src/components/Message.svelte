<script context="module" lang="ts">
    export function generateMessage(username: string, imgSrc: string, message: string) {
        return {
            username: username,
            imgSrc: imgSrc,
            message: message,
        };
    }
</script>

<script lang="ts">
    export let username = "Anonymous";

    export let imgSrc =
        "https://history.ucr.edu/sites/g/files/rcwecm1916/files/styles/form_preview/public/blank-profile-picture-png.png";

    export let message = "This is my message.";
    export let timestamp = "01/01/01 at 12:00 PM";
</script>

<div class="flex h-12 w-full mb-5">
    <img src={imgSrc} alt="Profile" class="w-12 rounded-full" />

    <div class="flex-col w-full ml-3">
        <p class="font-bold text-gray-200">
            {username}
            <span class="ml-2 italic font-mono font-thin text-gray-600 text-xs">{timestamp}</span>
        </p>
        <p>{message}</p>
    </div>
</div>
