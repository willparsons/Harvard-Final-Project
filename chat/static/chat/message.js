document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("#username").forEach(element => {
        const child = element.firstElementChild;
        child.addEventListener("click", () => getMessagesToUser(child.id));
    });
});

// TODO: we should definitely use react
function getMessagesToUser(user_id) {
    // d["messages"][idx]["fields"]["etc"]
    fetch(`messages/${user_id}`)
        .then(r => r.json())
        .then(data => {
            console.log(data);

            data["messages"].forEach(message => {
                const p = document.createElement("p");
                p.innerHTML = message["fields"]["content"];

                document.querySelector("#message-container").append(p);
            });
        });
}

