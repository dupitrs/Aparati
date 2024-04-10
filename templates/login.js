document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    // Fetch request to server to process login
    // On success:
    window.location.href = '/main_page';
});
