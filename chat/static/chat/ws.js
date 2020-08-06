const roomName = JSON.parse(document.getElementById('room-name').textContent);


// TODO: Reconnecting web socket
const chatSocket = new WebSocket(
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
            buildMultipleMessages(data["data"]);
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

document.querySelector('#chat-message-submit').onclick = function (e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'command': 'new_message',
        'data': message
    }));
    messageInputDom.value = '';
};


function messageString(message) {
    return `(${message.id}) ${message.author} @${message.timestamp}: ${message.content}\n`;
}

// Determine if we have an array
function buildMultipleMessages(messages) {
    messages.forEach(message => {
        buildMessage(message);
    });
}


function buildMessage(message) {
    const user = message.author;

    const article = document.createElement("article");
    article.className = "p-2 media";

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

    document.querySelector("#message-container").append(article);
}