init();

async function init() {
    const token = window.localStorage.getItem('token');

    const options = {
        method: "GET",
        headers: new Headers({
            'Authorization': `Bearer ${token}`,
            'Content-type': 'application/json',
        }),
    };

    const res = await fetch('/me', options);

    if (res.status === 200) {
        const json = await res.json();

        const imgElement = document.querySelector('#img');
        const nameElement = document.querySelector('#name');
        const emailElement = document.querySelector('#email');

        if (json.data.user.picture)
            imgElement.src = `data:image/png;base64, ${json.data.user.picture}`;
        nameElement.value = json.data.user.name;
        emailElement.value = json.data.user.email;
    } else {
        window.location.href = '/login';
    }

}

async function updateProfile(event) {
    event.preventDefault();

    const token = window.localStorage.getItem('token');

    const options = {
        method: "PATCH",
        headers: new Headers({
            'Authorization': `Bearer ${token}`,
        }),
        body: new FormData(profileForm)
    };

    const res = await fetch('/me', options);

    if (res.status === 200) {
        const profileFormSuccessElement = document.querySelector('#profileForm').querySelector('.success');
        profileFormSuccessElement.style.display = 'block';
        init();
    } else {
        const profileFormSuccessElement = document.querySelector('#profileForm').querySelector('.error');
        profileFormSuccessElement.style.display = 'block';
    }
}

async function deleteAccount(event) {
    event.preventDefault();

    const token = window.localStorage.getItem('token');

    const options = {
        method: "DELETE",
        headers: new Headers({
            'Authorization': `Bearer ${token}`,
            'Content-type': 'application/json',
        })
    };

    const res = await fetch('/me', options);

    if (res.status === 200) {
        window.localStorage.removeItem('token');
        window.location.href = '/login';
    }
}