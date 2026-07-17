/* ============================================================
   LBS AI Assistant
   script.js
   PART 1
============================================================ */

const chatBox = document.getElementById("chat-box");
const messageInput = document.getElementById("message");
const sendBtn = document.getElementById("send-btn");
const typingIndicator = document.getElementById("typing-indicator");
const suggestionsContainer = document.getElementById("suggestions-container");

/* ==========================================
            AUTO SCROLL
========================================== */

function scrollToBottom() {

    chatBox.scrollTo({
        top: chatBox.scrollHeight,
        behavior: "smooth"
    });

}

/* ==========================================
            CURRENT TIME
========================================== */

function getCurrentTime() {

    return new Date().toLocaleTimeString([], {

        hour: "2-digit",
        minute: "2-digit"

    });

}

/* ==========================================
        SHOW / HIDE TYPING
========================================== */

function showTyping() {

    typingIndicator.style.display = "flex";

    scrollToBottom();

}

function hideTyping() {

    typingIndicator.style.display = "none";

}

/* ==========================================
        CREATE USER MESSAGE
========================================== */

function addUserMessage(text) {

    const wrapper = document.createElement("div");

    wrapper.className = "user-message message";

    wrapper.innerHTML = `

        <div class="bubble">

            <div class="sender">
                You
            </div>

           <p>${escapeHTML(text)}</p>

            <div class="message-time">

                ${getCurrentTime()}

            </div>

        </div>

        <div class="avatar user-avatar">

            <i class="fa-solid fa-user"></i>

        </div>

    `;

    chatBox.appendChild(wrapper);

    scrollToBottom();

}

/* ==========================================
        CREATE BOT MESSAGE
========================================== */

function addBotMessage(text) {

    const wrapper = document.createElement("div");

    wrapper.className = "bot-message message";
    
    // Parse the Markdown into rich HTML elements
    const parsedHTML = marked.parse(text);

    wrapper.innerHTML = `

        <div class="avatar bot-avatar">

            <i class="fa-solid fa-robot"></i>

        </div>

        <div class="bubble">

            <div class="sender">

                AI Assistant

            </div>

           <div class="markdown-content">${parsedHTML}</div>

            <div class="message-time">

                ${getCurrentTime()}

            </div>

        </div>

    `;

    chatBox.appendChild(wrapper);

    scrollToBottom();

}

/* ==========================================
            DISABLE INPUT
========================================== */

function disableInput() {

    sendBtn.disabled = true;

    messageInput.disabled = true;

}

function enableInput() {

    sendBtn.disabled = false;

    messageInput.disabled = false;

    messageInput.focus();

}

/* ==========================================
            SEND MESSAGE
========================================== */

async function sendMessage() {

    const message = messageInput.value.trim();

    if (!message) return;

    suggestionsContainer.style.display = "none";

    addUserMessage(message);

    messageInput.value = "";

    disableInput();

    showTyping();

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

        hideTyping();

        addBotMessage(data.reply || data.error);

    }

    catch (error) {

        hideTyping();

        addBotMessage(

            "⚠️ Unable to connect to the server. Please try again."

        );

    }

    enableInput();

    scrollToBottom();

}

/* ============================================================
   PART 2
   Greeting • Suggestions • Clear Chat • Initialization
============================================================ */


/* ==========================================
            CLEAR CHAT
========================================== */

async function clearChat() {

    try {

        await fetch("/clear-history", {

            method: "POST"

        });

        chatBox.innerHTML = "";

        addBotMessage(
            "👋 Chat history cleared successfully. How may I assist you today?"
        );

        suggestionsContainer.style.display = "flex";

    }

    catch (error) {

        alert("Unable to clear chat.");

    }

}


/* ==========================================
            GREETING
========================================== */

function setGreeting() {

    const hour = new Date().getHours();

    let greeting = "";

    if (hour >= 5 && hour < 12) {

        greeting = "🌅 Good Morning";

    }

    else if (hour >= 12 && hour < 17) {

        greeting = "☀️ Good Afternoon";

    }

    else if (hour >= 17 && hour < 21) {

        greeting = "🌆 Good Evening";

    }

    else {

        greeting = "🌙 Good Night";

    }

    const greetingElement = document.getElementById("greeting");

    if (greetingElement) {

        greetingElement.textContent = greeting + " 👋";

    }

}


/* ==========================================
        CREATE SUGGESTION CHIP
========================================== */

function createSuggestionChip(text) {

    const chip = document.createElement("button");

    chip.className = "chip-btn";

    chip.textContent = text;

    chip.onclick = () => {

        messageInput.value = text;

        sendMessage();

    };

    return chip;

}


/* ==========================================
        LOAD SUGGESTIONS
========================================== */

async function loadSuggestions() {

    try {

        const response = await fetch("/suggestions");

        const suggestions = await response.json();

        suggestionsContainer.innerHTML = "";

        suggestions.forEach((item) => {

            suggestionsContainer.appendChild(

                createSuggestionChip(item)

            );

        });

    }

    catch (error) {

        console.log("Suggestions unavailable.");

    }

}


/* ==========================================
        ENTER KEY SUPPORT
========================================== */

messageInput.addEventListener("keydown", function(event){

    if(event.key==="Enter"){

        event.preventDefault();

        sendMessage();

    }

});


/* ==========================================
            AUTO FOCUS
========================================== */

window.addEventListener("load",()=>{

    messageInput.focus();

});


/* ==========================================
        OPTIONAL ESC SHORTCUT
========================================== */

document.addEventListener("keydown",function(e){

    if(e.key==="Escape"){

        messageInput.focus();

    }

});


/* ==========================================
        PREVENT DOUBLE CLICK
========================================== */

sendBtn.addEventListener("click",()=>{

    if(!sendBtn.disabled){

        sendMessage();

    }

});


/* ==========================================
            INITIALIZE
========================================== */

function initializeChatbot(){

    setGreeting();

    loadSuggestions();

    hideTyping();

    scrollToBottom();

}

initializeChatbot();


/* ==========================================
        OPTIONAL HELPERS
========================================== */

function showSuggestions(){

    suggestionsContainer.style.display="flex";

}

function hideSuggestions(){

    suggestionsContainer.style.display="none";

}


/* ==========================================
        OPTIONAL MARKDOWN SUPPORT
========================================== */

function escapeHTML(text){

    const div=document.createElement("div");

    div.textContent=text;

    return div.innerHTML;

}