function sendRequest(endpoint, usernameId, passwordId) {
    var username = document.getElementById(usernameId).value;
    var password = document.getElementById(passwordId).value;

    var formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Operation successful!');
            setTimeout(() => window.location.reload(), 1000);
        } else {
            alert('Operation failed. Please check your credentials.');
        }
    })
    .catch(error => console.error('Error:', error));
}

function login() {
    sendRequest('/', 'username', 'password');
}

function register() {
    sendRequest('/register', 'register_username', 'register_password');
}



