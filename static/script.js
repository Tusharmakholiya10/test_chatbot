async function sendMessage() {
    document.getElementById("suggestions-container").style.display = "none";
    const input = document.getElementById("message");
    const chatBox = document.getElementById("chat-box");

    const message = input.value.trim();
    
    if (!message) {
        return;
    }

    chatBox.innerHTML += `
        <div class="user-message">
            ${message}
        </div>
    `;

    input.value = "";

    chatBox.innerHTML += `
        <div class="bot-message" id="typing">
            Bot is typing...
        </div>
    `;

    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        document.getElementById("typing").remove();

        chatBox.innerHTML += `
            <div class="bot-message">
                ${data.reply || data.error}
            </div>
        `;

    } catch (error) {

        document.getElementById("typing").remove();

        chatBox.innerHTML += `
            <div class="bot-message">
                Unable to connect to server.
            </div>
        `;
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}

document.getElementById("message")
    .addEventListener("keypress", function(e) {

        if (e.key === "Enter") {
            sendMessage();
        }
    });
    async function clearChat() {
    try {
        await fetch("/clear-history", {
            method: "POST"
        });

        document.getElementById("chat-box").innerHTML = `
            <div class="bot-message">
                Chat cleared. How can I help you?
            </div>
        `;

    } catch (error) {
        alert("Unable to clear chat.");
    }
}

async function loadSuggestions() {

    const response = await fetch("/suggestions");
    const suggestions = await response.json();

    const container = document.getElementById("suggestions-container");

    suggestions.forEach(text => {

        const button = document.createElement("button");

        button.className = "chip";

        button.innerText = text;

        button.onclick = () => {

            document.getElementById("message").value = text;

            sendMessage();
        };

        container.appendChild(button);
    });
}

loadSuggestions();