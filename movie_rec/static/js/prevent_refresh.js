document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("register-form");

    if (!form) {
        console.log("Register form not found");
        return;
    }

    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const formData = new FormData(form);

        fetch("", {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        })
        .then(res => res.json())
        .then(data => {
            document.querySelectorAll(".error").forEach(e => e.remove());

            if (data.success) {
                window.location.href = "/login/";
            } else {
                for (const field in data.errors) {
                    const input = document.querySelector(`[name="${field}"]`);

                    if (!input) {
                        console.log("No input found for:", field);
                        continue;
                    }

                    data.errors[field].forEach(err => {
                        const p = document.createElement("p");
                        p.className = "error text-red-500 text-sm mb-2";
                        p.innerText = err.message;
                        input.insertAdjacentElement("afterend", p);
                    });
                }
            }
        })
        .catch(error => console.log("Fetch error:", error));
    });
});