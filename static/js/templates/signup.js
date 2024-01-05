async function login(event) {
    event.preventDefault();

    const fname = document.querySelector("#fname").value;
    const email = document.querySelector("#email").value;
    const password = document.querySelector("#password").value;

    const body = {
        fname: fname,
        email: email,
        password: password,
    };

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
        console.log(res.statusText);
    }
}
