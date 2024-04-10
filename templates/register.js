document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault();
    // Fetch request to server to process registration
    // On success:
    window.location.href = '/';
});
