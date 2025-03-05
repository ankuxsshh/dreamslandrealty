document.querySelectorAll(".btn-country").forEach(button => {
    button.addEventListener("click", function () {
        document.querySelectorAll(".btn-country").forEach(btn => btn.classList.remove("active"));
        this.classList.add("active");
    });
});
