document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#friend-search").onkeyup = (e) => {
        if (e.keyCode === 13) { // enter, return
            const user = e.target.value;
            addFriend(user);
        }
    }

    document.querySelectorAll("#accept").forEach(element => {
        const user = element.parentNode.id;
        element.addEventListener("click", (e) => acceptFriendRequest(e, user));
    });

    document.querySelectorAll("#reject").forEach(element => {
        const user = element.parentNode.id;
        element.addEventListener("click", (e) => rejectFriendRequest(e, user));
    });
});

function addFriend(user) {
    fetch(`friend/${user}/add/`)
        .then(r => r.json())
        .then(data => {
            if (data["error"]) {
                showAlert("error", data["error"], "#query-response");
            } else if (data["success"]) {
                showAlert("success", data["success"], "#query-response");
            }
        });
}

function acceptFriendRequest(event, user) {
    fetch(`friend/${user}/accept/`)
        .then(r => r.json())
        .then(data => {
            console.log(data);
        });
    hideElement(event.target.parentNode);

    incFriends();
    decFriendRequests();
}

function rejectFriendRequest(event, user) {
    fetch(`friend/${user}/reject/`)
        .then(r => r.json())
        .then(data => {
            console.log(data);
        });
    hideElement(event.target.parentNode);

    decFriendRequests();
}

function hideElement(element) {
    element.style.display = "none";
}

function incFriends() {
    const value = parseInt(document.querySelector("#friend-count").innerHTML) + 1;
    document.querySelector("#friend-count").innerHTML = value.toString();
}

function decFriendRequests() {
    const value = parseInt(document.querySelector("#fr-count").innerHTML) - 1;
    document.querySelector("#fr-count").innerHTML = value.toString();
}

function showAlert(alertType, message, endPoint) {
    const alert = document.createElement("div");

    alert.setAttribute("role", "alert");
    alert.innerHTML = message;

    if (alertType === "error") {
        alert.className = "alert alert-danger";
    } else if (alertType === "success") {
        alert.className = "alert alert-success";
    }

    document.querySelector(endPoint).innerHTML = "";
    document.querySelector(endPoint).append(alert);
}