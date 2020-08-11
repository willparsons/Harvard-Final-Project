// const roomName = JSON.parse(document.getElementById('room-name').textContent);

let chatSocket = undefined;

document.querySelectorAll("#room-name").forEach(element => {
    element.addEventListener("click", () => {
        setupWebSocket(element.children[0].id);
    });
});

function setupWebSocket(roomName) {
    if (chatSocket !== undefined) {
        closeWebSocket();
    }

    // todo: Reconnecting web socket
    chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/chat/'
        + roomName
        + '/'
    );

    chatSocket.onopen = function (e) {
        chatSocket.send(JSON.stringify({"command": "fetch_messages"}));
    }

    chatSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);

        switch (data["command"]) {
            case "fetch_messages":
                buildMultipleMessages(data["data"],);
                break;

            case "fetch_more_messages":
                buildMultipleMessages(data["data"], true);
                break;

            case "new_message":
                buildMessage(data["data"]);
                break;

            default:
                console.log("nothing");
                break;
        }
    };

    chatSocket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#chat-message-input').focus();
    document.querySelector('#chat-message-input').onkeyup = function (e) {
        if (e.keyCode === 13) {  // enter, return
            // document.querySelector('#chat-message-submit').click();
            const messageInputDom = document.querySelector('#chat-message-input');
            const message = messageInputDom.value;
            chatSocket.send(JSON.stringify({
                'command': 'new_message',
                'data': message
            }));
            messageInputDom.value = '';
        }
    };

    const messageContainer = document.querySelector("#message-container");
    messageContainer.addEventListener("scroll", (e) => {
        if (e.target.scrollTop === 0) {
            chatSocket.send(JSON.stringify({
                "command": "fetch_more_messages",
                "data": messageContainer.firstChild.id
            }));
        }
    });

    /*document.querySelector('#chat-message-submit').onclick = function (e) {
        const messageInputDom = document.querySelector('#chat-message-input');
        const message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'command': 'new_message',
            'data': message
        }));
        messageInputDom.value = '';
    };*/
}

function closeWebSocket() {
    chatSocket.close();
    document.querySelector("#message-container").innerHTML = "";
}

function buildMultipleMessages(messages, prepend = false) {
    messages.forEach(message => {
        buildMessage(message, prepend);
    });
}

function buildMessage(message, prepend) {
    const user = message.author;

    const article = document.createElement("article");
    article.className = "p-2 media";
    article.id = message.id;

    const img = document.createElement("img");
    img.className = "rounded-circle article-img mr-3";
    img.src = message.image;
    img.alt = "profile image";

    const mediaBody = document.createElement("div");
    mediaBody.className = "media-body";

    const messageContent = document.createElement("p");
    messageContent.innerHTML = message.content;
    messageContent.id = "message";

    const metadata = document.createElement("div");
    metadata.className = "article-metadata";

    const userLink = document.createElement("a");
    userLink.className = "mr-2";
    userLink.href = "#";
    userLink.innerHTML = user;

    const timestamp = document.createElement("small");
    timestamp.className = "text-muted";
    timestamp.id = "timestamp";
    timestamp.innerHTML = message.timestamp;

    metadata.append(userLink);
    metadata.append(timestamp);

    mediaBody.append(metadata);
    mediaBody.append(messageContent);

    article.append(img);
    article.append(mediaBody);

    const messageContainer = document.querySelector("#message-container");

    if (prepend) {
        messageContainer.prepend(article);
    } else {
        messageContainer.append(article);
        messageContainer.scrollTop = messageContainer.scrollHeight;
    }

}