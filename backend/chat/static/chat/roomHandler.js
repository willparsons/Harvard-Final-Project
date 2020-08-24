document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#createRoomForm").addEventListener("submit", (e) => createRoom(e));
});

function createRoom(e) {
    e.preventDefault();

    const data = new FormData(e.target);

    const display_name = data.get("display-name");
    const participants = data.getAll("participants").join(";");

    fetch(`/room/create/${display_name}/${participants}/`)
        .then(r => r.json())
        .then(data => {
            if (data["error"]) {
                showAlert("error", data["error"], "#create-room-response");
            } else if (data["success"]) {
                showAlert("success", data["success"], "#create-room-response");
            }
        });
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
