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
            if (response.headers.get("content-type").startsWith("audio")) {
                return { type: "audio", data: response.blob() };
            } else if (
                response.headers.get("content-type").startsWith("video")
            ) {
                return { type: "video", data: response.blob() };
            } else {
                return { type: "summary", data: response.json() };
            }
        })
        .then(({ type, data }) => {
            hideLoader();
            // Handle the API response data here
            if (type == "audio" || type == "video") {
                data.then((blob) => {
                    const mediaContainer =
                        document.getElementById("mediaContainer");
                    mediaContainer.hidden = false;
                    mediaContainer.innerHTML = "";
                    const url = URL.createObjectURL(blob);
                    const mediaElement = document.createElement(type);
                    mediaElement.controls = true;
                    mediaElement.src = url;
                    mediaContainer.appendChild(mediaElement);
                });
            } else {
                
                const outputArea = document.getElementById("output-area");
                data.then((data) => {

                    switch (type) {
                        case "summary":
                            outputArea.innerHTML = `<h3 class="text-xl font-bold mb-2">Summary:</h3><p>${data.content}</p>`;
                            break;
                        case "quiz":
                            outputArea.innerHTML = `<h3 class="text-xl font-bold mb-2">Quiz:</h3>${data.content}`;
                            break;
                        default:
                            outputArea.innerHTML = `<p>Unsupported response type: ${type}</p>`;
                    }
                });
            }
        })
        .catch((error) => {
            // Handle errors here
            console.error("There was a problem with the API request:", error);
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
