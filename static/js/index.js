const loader = document.getElementById("loader");
loader.hidden = true;
tailwind.config = {
    darkMode: "class",
};
function toggleTheme() {
    const html = document.documentElement;
    html.classList.toggle("dark");
}

function showLoader() {
    const loader = document.getElementById("loader");
    loader.hidden = false;
}

function hideLoader() {
    const loader = document.getElementById("loader");
    loader.hidden = true;
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
                return { type: "quiz-generation", data: response.json() };
            }
        })
        .then(({ type, data }) => {
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
                        case "quiz-generation":
                            const quizContainer = document.createElement("div");
                            quizContainer.classList.add(
                                "flex",
                                "flex-col",
                                "gap-4"
                            );

                            data.content.forEach(
                                (questionData, index) => {
                                    const questionCard =
                                        document.createElement("div");
                                    questionCard.classList.add(
                                        "p-4",
                                        "bg-gray-100",
                                        "rounded",
                                        "shadow"
                                    );

                                    const questionNumber =
                                        document.createElement("h2");
                                    questionNumber.classList.add(
                                        "text-lg",
                                        "font-bold",
                                        "mb-2"
                                    );
                                    questionNumber.textContent =
                                        questionData.question;

                                    const optionsList =
                                        document.createElement("ul");
                                    optionsList.classList.add(
                                        "list-disc",
                                        "ml-6"
                                    );

                                    for (let i = 1; i <= 4; i++) {
                                        const optionKey = 'option' + i;
                                        if (questionData.hasOwnProperty(optionKey)) {
                                            const optionItem = document.createElement('li');
                                            optionItem.textContent = questionData[optionKey];
                                            optionsList.appendChild(optionItem);
                                        }
                                    }

                                    questionCard.appendChild(questionNumber);
                                    questionCard.appendChild(optionsList);
                                    quizContainer.appendChild(questionCard);
                                }
                            );

                            outputArea.appendChild(quizContainer);
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
        .finally(() => {
            hideLoader();
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
// handleButtonClick("summary-btn", "/summary");
handleButtonClick("video-btn", "/video");
//handleButtonClick("audio-btn", "/audio");
handleButtonClick("quiz-btn", "/quiz-generation");
