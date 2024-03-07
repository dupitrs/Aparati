// static/app.js

function authenticate() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: username, password: password }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Login successful!');
            // Redirect or perform other actions after successful login
        } else {
            alert('Login failed. Please check your credentials.');
        }
    });
}

function register() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: username, password: password }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Registration successful!');
            // Redirect or perform other actions after successful registration
        } else {
            alert('Registration failed. Please try a different username.');
        }
    });
}
