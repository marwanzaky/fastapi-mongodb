async function login(event) {
    event.preventDefault();

    const name = document.querySelector("#name").value;
    const email = document.querySelector("#email").value;
    const password = document.querySelector("#password").value;
    const passwordConfirm = document.querySelector("#passwordConfirm").value;

    const body = { name, email, password, "password_confirm": passwordConfirm };

    const res = await fetch("/signup", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
    });


    if (res.status === 201) {
        window.location.href = "/login";
    } else {
        const json = await res.json();

        const formErrorElement = document.querySelector(".form .error");
        formErrorElement.style.display = "block";
        formErrorElement.textContent = json.detail;
    }
}
