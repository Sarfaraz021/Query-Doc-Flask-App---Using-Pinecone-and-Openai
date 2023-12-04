document.addEventListener("DOMContentLoaded", function () {
    const uploadForm = document.getElementById("uploadForm");
    const chatContainer = document.getElementById("chatContainer");
    const chatMessages = document.getElementById("chatMessages");
    const userInput = document.getElementById("userInput");
    const sendMessageBtn = document.getElementById("sendMessage");

    uploadForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = new FormData(this);

        fetch("/chat", {
            method: "POST",
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            // Handle the AI response
            const aiResponse = data.ai_response;
            displayMessage("AI", aiResponse);
        })
        .catch(error => {
            console.error("Error:", error);
        });

        chatContainer.style.display = "block";
        uploadForm.style.display = "none";
    });

    sendMessageBtn.addEventListener("click", function () {
        const userMessage = userInput.value;
        if (userMessage.trim() === "") return;

        // Display user message in the chat
        displayMessage("You", userMessage);

        // Send user message to the server and get AI response
        fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ user_message: userMessage }),
        })
        .then(response => response.json())
        .then(data => {
            // Handle the AI response
            const aiResponse = data.ai_response;
            displayMessage("AI", aiResponse);
        })
        .catch(error => {
            console.error("Error:", error);
        });

        // Clear the input field
        userInput.value = "";
    });

    function displayMessage(sender, message) {
        const messageDiv = document.createElement("div");
        messageDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatMessages.appendChild(messageDiv);

        // Scroll to the bottom to show the latest message
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
