async function login(event) {
    event.preventDefault();

    const email = document.querySelector("#email").value;
    const password = document.querySelector("#password").value;

    const body = {
        email: email,
        password: password,
    };

    const res = await fetch("/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
    });

    if (res.status === 200) {
        const json = await res.json();

        window.localStorage.setItem("token", json.data.access_token);
        window.location.href = "/";
    } else {
        const formErrorElement = document.querySelector(".form .error");
        formErrorElement.style.display = "block";
    }
}
