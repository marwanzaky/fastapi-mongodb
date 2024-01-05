(async function () {
    const token = window.localStorage.getItem("token");

    const options = {
        method: "GET",
        headers: new Headers({
            Authorization: `Bearer ${token}`,
            "Content-type": "application/json",
        }),
    };

    const res = await fetch("/me", options);

    if (res.status === 200) {
        const json = await res.json();
        const h1Element = document.querySelector("#h1");

        h1Element.textContent = `Welcome, ${json.data.user.fname}`;
    } else {
        window.location.href = "/login";
    }
})();

function logout() {
    window.localStorage.removeItem("token");
}
