document.addEventListener("DOMContentLoaded", function () { 
    const textareas = document.querySelectorAll(".auto-expand");


    textareas.forEach(function (textarea) {
        textareas.addEventListener("input", function () {
            textarea.style.height = "auto";
            textarea.style.height = textarea.scrollHeigh + "px"
        });
    });
});