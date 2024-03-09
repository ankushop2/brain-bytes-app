tailwind.config = {
    darkMode: "class",
};
function toggleTheme() {
    const html = document.documentElement;
    html.classList.toggle("dark");
}


const loader = document.querySelector('#loader');

function showLoader() {
  loader.classList.remove('hidden');
}

function hideLoader() {
  loader.classList.add('hidden');
}

// Call showLoader() before making the API call
// Call hideLoader() after receiving the response

// Example usage:
showLoader();

// Function to make API call
function makeAPICall(apiUrl, data) {
    // Your API call implementation here
    showLoader();
    fetch(apiUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then((data) => {
            // Handle the API response data here
            hideLoader();
            const outputArea = document.getElementById('output-area');
            outputArea.innerHTML += JSON.stringify(data);
        })
        .catch((error) => {
            // Handle errors here
            console.error("There was a problem with the API request:", error);
            
        }).finally(() => {
            
        });
}

// Function to handle button click
function handleButtonClick(buttonId, endpoint) {
    document.getElementById(buttonId).addEventListener("click", function () {
        const currentUrl = window.location.href;
        const apiUrl = currentUrl + endpoint;
        const inputUrl = document.getElementById("url-input").value;
        const requestData = { URL: inputUrl };
        makeAPICall(apiUrl, requestData);
    });
}


// Attaching event listeners to buttons
handleButtonClick("summary-btn", "/summary");
handleButtonClick("video-btn", "/video");
handleButtonClick("audio-btn", "/audio");
handleButtonClick("quiz-btn", "/quiz");
