document.addEventListener("DOMContentLoaded", () => {
    const links = document.querySelectorAll(".nav-link");
    const page = window.location.pathname;

    links.forEach(link => {
        if (link.pathname === page) {
            link.classList.add("active");
        } else {
            link.classList.remove("active");
        }
    });
});
