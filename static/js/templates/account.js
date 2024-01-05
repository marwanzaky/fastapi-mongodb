(async function () {
    const token = window.localStorage.getItem('token');

    const options = {
        method: "GET",
        headers: new Headers({
            'Authorization': `Bearer ${token}`, 
            'Content-type': 'application/json',
        }), 
    };

    const res = await fetch('/me', options);

    if(res.status === 200) {
        const json = await res.json();

        const fnameElement = document.querySelector('#fname');
        const emailElement = document.querySelector('#email');

        fnameElement.value = json.data.user.fname;
        emailElement.value = json.data.user.email;
    } else {
        window.location.href = '/login';
    }

})();

async function updateProfile(event) {
    event.preventDefault();

    const fname = document.querySelector('#fname').value;
    const email = document.querySelector('#email').value;

    const body = { fname, email };

    const token = window.localStorage.getItem('token');

    const options = {
        method: "PATCH",
        headers: new Headers({
            'Authorization': `Bearer ${token}`, 
            'Content-type': 'application/json',
        }),
        body: JSON.stringify(body)
    };

    const res = await fetch('/me', options);

    if(res.status === 200) {
        const profileFormSuccessElement = document.querySelector('#profile-form').querySelector('.success');
        profileFormSuccessElement.style.display = 'block';
    } else {
        const profileFormSuccessElement = document.querySelector('#profile-form').querySelector('.error');
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

    if(res.status === 200) {
        window.localStorage.removeItem('token');
        window.location.href = '/login';
    }
}