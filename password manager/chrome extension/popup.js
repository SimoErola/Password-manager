document.getElementById('saveButton').addEventListener('click', function() {
    let user = document.getElementById('usernameInput').value;
    let password = document.getElementById('passwordInput').value;
    browser.runtime.sendMessage({ action: 'savePassword', user: user, password: password });
});
