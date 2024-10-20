document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");

    sendBtn.addEventListener("click", async () => {
        const message = userInput.value.trim();
        
        if (message) {
            // Display user message
            appendMessage("User", message, "user-message");
            
            // Clear the input field
            userInput.value = "";

            // Send user message to the backend bot
            const botResponse = await getBotResponse(message);
            
            // Display bot response
            appendMessage("Bot", botResponse, "bot-message");
        }
    });

    function appendMessage(sender, message, className) {
        const messageElement = document.createElement("p");
        messageElement.classList.add(className);
        messageElement.textContent = `${sender}: ${message}`;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
    }

    // Function to get bot response (replace with actual backend call)
    async function getBotResponse(message) {
        try {
            const response = await fetch("http://127.0.0.1:8000/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ message }),
            });
            const data = await response.json();
            return data.reply;  // The bot's reply from backend
        } catch (error) {
            console.error("Error fetching bot response:", error);
            return "Sorry, I couldn't connect to the server.";
        }
    }
    
        
});

