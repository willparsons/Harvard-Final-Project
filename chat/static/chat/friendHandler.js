document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#friend-search").onkeyup = (e) => {
        if (e.keyCode === 13) { // enter, return
            const user = e.target.value;
            addFriend(user);
        }
    }

    document.querySelector("#add-button").addEventListener("click", () => {
        const user = document.querySelector("#friend-search").value;
        addFriend(user);
    });

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
    fetch(`/friend/${user}/add/`)
        .then(r => r.json())
        .then(data => {
            if (data["error"]) {
                showAlert("error", data["error"], "#friend-request-response");
            } else if (data["success"]) {
                showAlert("success", data["success"], "#friend-request-response");
            }
        });
}

function acceptFriendRequest(event, user) {
    fetch(`/friend/${user}/accept/`)
        .then(r => r.json())
        .then(data => {
            console.log(data);
        });

    updateFriendRequests(user);
    updateFriendsList(user);
}

function rejectFriendRequest(event, user) {
    fetch(`/friend/${user}/reject/`)
        .then(r => r.json())
        .then(data => {
            console.log(data);
        });

    updateFriendRequests(user);
}

function updateFriendsList(user) {
    const li = document.createElement("li");
    li.id = user;
    li.innerHTML = user;

    hideElement("#allFriendsPlaceholder");
    document.querySelector("#allFriendsList").append(li);
}

function updateFriendRequests(user) {
    deleteElement(`#${user}`);
}

function hideElement(element) {
    document.querySelector(element).style.display = "none";
}


function deleteElement(element) {
    console.log(document.querySelector(element).parentNode);
    document.querySelector(element).parentNode.removeChild(document.querySelector(element));
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
