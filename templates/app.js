// app.js
document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission
    register();
});

document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission
    authenticate();
});

function authenticate() {
    var username = document.getElementById('login_username').value;
    var password = document.getElementById('login_password').value;

    var formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Login successful!');
            window.location.reload();
        } else {
            alert('Login failed. Please check your credentials.');
        }
    })
    .catch(error => console.error('Error:', error));
}

function register() {
    var username = document.getElementById('register_username').value;
    var password = document.getElementById('register_password').value;

    var formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            var modal = document.getElementById('successModal');
            modal.style.display = 'block'; // Show the success modal
            setTimeout(function() {
                modal.style.display = 'none';
                window.location.reload(); // Reload the page after 3 seconds
            }, 3000);
        } else {
            alert('Registration failed. Please try a different username.');
        }
    })
    .catch(error => console.error('Error:', error));
}
