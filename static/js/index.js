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
                data.then((response) => {
                    const type = response.type;
                    let content;

                    switch (type) {
                        case "quiz-generation":
                            try {
                                // Remove the outer double quotes and unescape the JSON string
                                content = JSON.parse(response.content);
                            } catch (error) {
                                outputArea.innerHTML = `<p>Invalid JSON format in the API response.</p>`;
                                return;
                            }
                            const quizContainer = document.createElement("div");
                            quizContainer.classList.add(
                                "flex",
                                "flex-col",
                                "gap-4"
                            );

                            const quizData = Object.entries(content);

                            quizData.forEach(([key, value], index) => {
                                if (key.startsWith("Question")) {
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
                                    questionNumber.textContent = value;

                                    const optionsList =
                                        document.createElement("div");
                                    optionsList.classList.add(
                                        "flex",
                                        "flex-col",
                                        "gap-2"
                                    );

                                    const answerKey = content[`Answer`];
                                    let optionIndex = index * 5 + 1;
                                    for (let i = 1; i <= 4; i++) {
                                        const optionKey = `Option ${i}`;
                                        const optionValue = content[optionKey];

                                        if (optionValue) {
                                            const optionItem =
                                                document.createElement("div");
                                            optionItem.classList.add(
                                                "flex",
                                                "items-center"
                                            );

                                            const optionRadio =
                                                document.createElement("input");
                                            optionRadio.type = "radio";
                                            optionRadio.name = `question-${index}`;
                                            optionRadio.value = optionValue;

                                            const optionLabel =
                                                document.createElement("label");
                                            optionLabel.classList.add("ml-2");
                                            optionLabel.textContent =
                                                optionValue;

                                            optionItem.appendChild(optionRadio);
                                            optionItem.appendChild(optionLabel);
                                            optionsList.appendChild(optionItem);
                                        }

                                        optionIndex++;
                                    }

                                    const answerFeedback =
                                        document.createElement("p");
                                    answerFeedback.classList.add(
                                        "text-green-500",
                                        "font-bold",
                                        "mt-2"
                                    );
                                    answerFeedback.textContent = `Correct Answer: ${answerKey}`;
                                    answerFeedback.style.display = "none";
                                    optionsList.addEventListener(
                                        "change",
                                        () => {
                                            const selectedOption = Array.from(
                                                optionsList.querySelectorAll(
                                                    "input"
                                                )
                                            ).find((input) => input.checked);
                                            if (
                                                selectedOption &&
                                                selectedOption.value ===
                                                    content[answerKey]
                                            ) {
                                                answerFeedback.style.display =
                                                    "block";
                                            } else {
                                                answerFeedback.style.display =
                                                    "none";
                                            }
                                        }
                                    );

                                    questionCard.appendChild(questionNumber);
                                    questionCard.appendChild(optionsList);
                                    questionCard.appendChild(answerFeedback);
                                    quizContainer.appendChild(questionCard);
                                }
                            });

                            outputArea.appendChild(quizContainer);
                            break;
                        case "summary":
                            // Create tab container
                            var tabContainer = document.createElement("div");
                            tabContainer.className = "mt-4";

                            enHeader = document.createElement("h2");
                            enHeader.className = "text-xl font-bold mb-4"
                            enHeader.innerHTML = "English: ";
                            enContent = document.createElement("p");
                            enContent.innerHTML = response.content.summary_en;

                            frHeader = document.createElement("h2");
                            frHeader.className = "text-xl font-bold mb-4"
                            frHeader.innerHTML = "French: ";
                            frContent = document.createElement("p");
                            frContent.innerHTML = response.content.summary_fr;

                            itHeader = document.createElement("h2");
                            itHeader.className = "text-xl font-bold mb-4"
                            itHeader.innerHTML = "Italian: ";
                            itContent = document.createElement("p");
                            itContent.innerHTML = response.content.summary_it;

                            tabContainer.appendChild(enHeader);
                            tabContainer.appendChild(enContent);
                            tabContainer.appendChild(frHeader);
                            tabContainer.appendChild(frContent);
                            tabContainer.appendChild(itHeader);
                            tabContainer.appendChild(itContent);

                            outputArea.appendChild(tabContainer);
                            break;
                        case "flash-cards":
                            const cleanedContentText = response.content.replace(
                                /\\n/g,
                                ""
                            );

                            // Parse the cleaned text into JSON data
                            const jsonData = JSON.parse(cleanedContentText);

                            // Create the flip card container
                            const flipCard = document.createElement("div");
                            flipCard.className = "flip-card";

                            // Create the flip card inner container
                            const flipCardInner = document.createElement("div");
                            flipCardInner.className =
                                "flip-card-inner bg-gray-200 rounded-lg p-8 flex flex-col items-center justify-center";

                            // Create the flip card front
                            const flipCardFront = document.createElement("div");
                            flipCardFront.className = "flip-card-front";

                            const flipCardFrontH3 =
                                document.createElement("h3");
                            flipCardFrontH3.className =
                                "text-2xl font-bold mb-4";
                            flipCardFrontH3.textContent = "Flashcard";

                            const flipCardFrontP = document.createElement("p");
                            flipCardFrontP.className = "text-lg";
                            flipCardFrontP.textContent =
                                jsonData.Question1;

                            // Create the flip card back
                            const flipCardBack = document.createElement("div");
                            flipCardBack.className =
                                "flip-card-back bg-gray-300 rounded-lg p-8 flex flex-col items-center justify-center";

                            const flipCardBackH3 = document.createElement("h3");
                            flipCardBackH3.className =
                                "text-2xl font-bold mb-4";
                            flipCardBackH3.textContent = "Flashcard 1";

                            const flipCardBackP = document.createElement("p");
                            flipCardBackP.className = "text-lg";
                            flipCardBackP.textContent =
                                jsonData.Answer1;

                            // Append the front and back to the inner container
                            flipCardFront.appendChild(flipCardFrontH3);
                            flipCardFront.appendChild(flipCardFrontP);
                            flipCardInner.appendChild(flipCardFront);

                            flipCardBack.appendChild(flipCardBackH3);
                            flipCardBack.appendChild(flipCardBackP);
                            flipCardInner.appendChild(flipCardBack);

                            // Append the inner container to the flip card container
                            flipCard.appendChild(flipCardInner);

                            outputArea.appendChild(flipCard);
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
handleButtonClick("summary-btn", "/summary");
handleButtonClick("video-btn", "/video");
handleButtonClick("audio-btn", "/audio");
handleButtonClick("quiz-btn", "/quiz-generation");
handleButtonClick("flashcard-btn", "/flash-cards");
