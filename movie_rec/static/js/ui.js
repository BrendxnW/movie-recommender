document.addEventListener("DOMContentLoaded", function () { 
    const textareas = document.querySelectorAll(".auto-expand");


    textareas.forEach(function (textarea) {
        const resizeTextarea = function () {
            textarea.style.height = "auto";
            textarea.style.height = textarea.scrollHeight + "px";
        };

        resizeTextarea();
        textarea.addEventListener("input", resizeTextarea);
    });
});
