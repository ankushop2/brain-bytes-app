tailwind.config = {
    darkMode: "class",
};
function toggleTheme() {
    const html = document.documentElement;
    html.classList.toggle("dark");
}

const loader = document.querySelector("#loader");

function showLoader() {
    loader.classList.remove("hidden");
}

function hideLoader() {
    loader.classList.add("hidden");
}


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
            const { type, content } = data;
            hideLoader();
            const outputArea = document.getElementById("output-area");
        })
        .catch((error) => {
            // Handle errors here
            console.error("There was a problem with the API request:", error);
            switch (type) {
                case "summary":
                    outputArea.innerHTML = `<h3 class="text-xl font-bold mb-2">Summary:</h3><p>${content}</p>`;
                    break;
                case "video":
                    outputArea.innerHTML = `<h3 class="text-xl font-bold mb-2">Video:</h3><video src="${content}" controls></video>`;
                    break;
                case "audio":
                    outputArea.innerHTML = `<h3 class="text-xl font-bold mb-2">Audio:</h3><audio src="${content}" controls></audio>`;
                    break;
                case "quiz":
                    outputArea.innerHTML = `<h3 class="text-xl font-bold mb-2">Quiz:</h3>${content}`;
                    break;
                default:
                    outputArea.innerHTML = `<p>Unsupported response type: ${type}</p>`;
            }
        })
        .finally(() => {});
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
