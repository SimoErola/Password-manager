// Add a message listener to the background script

function getMainDomain(hostname) {
    let parts = hostname.split('.').reverse();
    if (parts != null && parts.length > 1) {
        return parts[1] + '.' + parts[0];
    }
    return hostname;
}

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === 'getSavedPassword') {
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            let currentTab = tabs[0];
            if (!currentTab || !currentTab.url || currentTab.url.startsWith('chrome://')) {
                console.error('Cannot fetch password: Invalid tab URL');
                return;
            }
            let url = new URL(currentTab.url);
            let site = getMainDomain(url.hostname);

            // Make an HTTP GET request to the localhost:5000 server
            fetch('https://localhost:5000/get_password?site=' + site)
                .then(response => response.json())
                .then(data => {
                    // Send a message to the content script with the username and password
                    chrome.tabs.sendMessage(currentTab.id, { action: 'autofill', user: data.user, password: data.password });
                })
                .catch(error => {
                    console.error('Error fetching password:', error);
                });
        });

        return true;  // Respond asynchronously
    }
});

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === 'savePassword') {
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            console.log(tabs);  // Log the entire tabs array
            let currentTab = tabs[0];
            let url = new URL(currentTab.url);
            let site = getMainDomain(url.hostname);
            let user = request.user;
            let password = request.password;
            fetch('https://localhost:5000/save_password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ site: site, user: user, password: password })
            })
                .then(response => response.json())
                .then(data => {
                    console.log(data.message);
                })
                .catch(error => {
                    console.error('Error saving password:', error);
                });
        });

        return true;  // Respond asynchronously
    }
});
