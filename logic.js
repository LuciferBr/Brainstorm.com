// Categorized inspirational responses
const responses = {
    climate: ["Inspiring action on climate change starts with stories..."],
    technology: ["Technology is the catalyst for transformation..."],
    sustainability: ["Sustainability is the foundation of progress..."],
    unity: ["True transformation comes from unity..."],
    youth: ["Youth are creating change..."],
    education: ["Education unlocks potential..."],
    equality: ["Equality means every voice is heard..."],
    collective: ["Collective will is our strongest tool..."],
    peace: ["Peace starts with kindness..."],
    local: ["Global change begins locally..."],
    mental: ["Mental health matters...", "Self-care is key...", "It’s okay to struggle..."]
};

// Keywords mapped to categories
const keywords = {
    climate: ["climate", "global warming", "environment"],
    technology: ["technology", "innovation", "tech"],
    sustainability: ["sustainability", "green", "renewable"],
    unity: ["unity", "global", "together"],
    youth: ["youth", "young", "future"],
    education: ["education", "learning", "knowledge"],
    equality: ["equality", "justice", "fairness"],
    collective: ["collective", "together", "humanity"],
    peace: ["peace", "harmony", "kindness"],
    local: ["local", "community", "action"],
    mental: ["mental health", "self-care", "judgment", "healing", "okay"]
};

// Flatten all responses for "all" category
const allResponses = Object.values(responses).flat();

// Chat functions (for igc.html)
function displayMessage(message, sender) {
    const chatBox = document.getElementById("chatBox");
    if (chatBox) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender);
        messageDiv.textContent = message;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

function getResponse(userInput, categoryFilter) {
    userInput = userInput.toLowerCase();
    let applicableResponses = categoryFilter === "all" ? allResponses : responses[categoryFilter] || allResponses;
    for (const [category, keyList] of Object.entries(keywords)) {
        if (keyList.some(key => userInput.includes(key))) {
            if (categoryFilter === "all" || categoryFilter === category) {
                return responses[category][Math.floor(Math.random() * responses[category].length)];
            }
        }
    }
    return applicableResponses.length > 0
        ? applicableResponses[Math.floor(Math.random() * applicableResponses.length)]
        : "Ask me about climate, equality, or mental health!";
}

function sendMessage() {
    const userInput = document.getElementById("userInput");
    if (userInput && userInput.value.trim()) {
        const inputValue = userInput.value.trim();
        displayMessage(inputValue, "user");
        userInput.value = "";
        const categoryFilter = document.getElementById("categoryFilter").value;
        const response = getResponse(inputValue, categoryFilter);
        displayMessage(response, "ai");
    }
}

function clearChat() {
    const chatBox = document.getElementById("chatBox");
    if (chatBox) {
        chatBox.innerHTML = "";
    }
}

function saveChat() {
    const chatBox = document.getElementById("chatBox");
    if (chatBox) {
        const chatContent = chatBox.textContent;
        const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
        const filename = `brainstorm_chat_${timestamp}.txt`;
        const blob = new Blob([chatContent], { type: "text/plain" });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = filename;
        link.click();
        URL.revokeObjectURL(url);
        displayMessage(`Chat saved as ${filename}`, "ai");
    }
}

// Game functions (for game.html)
function displayGameOutput(output) {
    const gameArea = document.getElementById("gameArea");
    if (gameArea) {
        const outputDiv = document.createElement("div");
        outputDiv.classList.add("game-output");
        outputDiv.textContent = output;
        gameArea.appendChild(outputDiv);
        gameArea.scrollTop = gameArea.scrollHeight;
    }
}

function playGame() {
    const gameInput = document.getElementById("gameInput");
    if (gameInput && gameInput.value.trim()) {
        const userInput = gameInput.value.trim();
        const gameType = document.getElementById("gameSelect").value;
        displayGameOutput(`Your input: ${userInput}`);
        let response;
        if (gameType === "wordAssociation") {
            const words = userInput.split(" ");
            const options = ["hope", "action", "nature", "unity"];
            response = `Associated idea: ${words[Math.floor(Math.random() * words.length)]} + ${options[Math.floor(Math.random() * options.length)]}`;
        } else if (gameType === "ideaChain") {
            const options = ["community", "innovation", "sustainability", "peace"];
            response = `Next in chain: ${userInput} → ${options[Math.floor(Math.random() * options.length)]}`;
        } else if (gameType === "whatIf") {
            const options = ["global peace", "clean energy", "equal opportunities"];
            response = `What if ${userInput} led to ${options[Math.floor(Math.random() * options.length)]}?`;
        }
        displayGameOutput(response);
        gameInput.value = "";
    }
}

function clearGame() {
    const gameArea = document.getElementById("gameArea");
    if (gameArea) {
        gameArea.innerHTML = "";
    }
}

// Theme toggle (for all pages)
function toggleTheme() {
    const body = document.body;
    const themeToggle = document.getElementById("themeToggle");
    if (body && themeToggle) {
        body.classList.toggle("dark-theme");
        if (body.classList.contains("dark-theme")) {
            localStorage.setItem("theme", "dark");
            themeToggle.textContent = "Light Mode";
        } else {
            localStorage.setItem("theme", "light");
            themeToggle.textContent = "Dark Mode";
        }
    }
}

// Initialize theme (for all pages)
const savedTheme = localStorage.getItem("theme");
const themeToggle = document.getElementById("themeToggle");
if (themeToggle) {
    if (savedTheme === "dark") {
        document.body.classList.add("dark-theme");
        themeToggle.textContent = "Light Mode";
    } else {
        themeToggle.textContent = "Dark Mode";
    }
}

// Bind events dynamically based on page content
function bindEvents() {
    // Theme toggle (all pages)
    const themeToggle = document.getElementById("themeToggle");
    if (themeToggle) {
        themeToggle.addEventListener("click", toggleTheme);
    }

    // IGC page events
    const sendButton = document.getElementById("sendButton");
    if (sendButton) {
        sendButton.addEventListener("click", sendMessage);
    }

    const clearChatButton = document.getElementById("clearChat");
    if (clearChatButton) {
        clearChatButton.addEventListener("click", clearChat);
    }

    const saveChatButton = document.getElementById("saveChat");
    if (saveChatButton) {
        saveChatButton.addEventListener("click", saveChat);
    }

    const userInput = document.getElementById("userInput");
    if (userInput) {
        userInput.addEventListener("keypress", (e) => {
            if (e.key === "Enter") sendMessage();
        });
    }

    // Game page events
    const playGameButton = document.getElementById("playGame");
    if (playGameButton) {
        playGameButton.addEventListener("click", playGame);
    }

    const clearGameButton = document.getElementById("clearGame");
    if (clearGameButton) {
        clearGameButton.addEventListener("click", clearGame);
    }

    const gameInput = document.getElementById("gameInput");
    if (gameInput) {
        gameInput.addEventListener("keypress", (e) => {
            if (e.key === "Enter") playGame();
        });
    }
}

// Run when the DOM is fully loaded
document.addEventListener("DOMContentLoaded", bindEvents);