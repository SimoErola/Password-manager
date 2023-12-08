chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === 'autofill') {
        // Try different selectors for the username field
        let userField = document.querySelector('input[name="username"], input[name="user"], input[name="email"], input[id="username"], input[id="user"], input[id="email"]');
        // Try different selectors for the password field
        let passwordField = document.querySelector('input[type="password"], input[name="password"], input[id="password"]');
        if (userField) {
            userField.value = request.user;
        }
        if (passwordField) {
            passwordField.value = request.password;
        }
    }
});