from pyscript import document, console
import random
from datetime import datetime
from js import document as js_doc, window, Blob, URL

# Categorized inspirational responses (shortened for brevity)
responses = {
    "climate": ["Inspiring action on climate change starts with stories..."],
    "technology": ["Technology is the catalyst for transformation..."],
    "sustainability": ["Sustainability is the foundation of progress..."],
    "unity": ["True transformation comes from unity..."],
    "youth": ["Youth are creating change..."],
    "education": ["Education unlocks potential..."],
    "equality": ["Equality means every voice is heard..."],
    "collective": ["Collective will is our strongest tool..."],
    "peace": ["Peace starts with kindness..."],
    "local": ["Global change begins locally..."],
    "mental": ["Mental health matters...", "Self-care is key...", "It’s okay to struggle..."]
}

keywords = {
    "climate": ["climate", "global warming", "environment"],
    "technology": ["technology", "innovation", "tech"],
    "sustainability": ["sustainability", "green", "renewable"],
    "unity": ["unity", "global", "together"],
    "youth": ["youth", "young", "future"],
    "education": ["education", "learning", "knowledge"],
    "equality": ["equality", "justice", "fairness"],
    "collective": ["collective", "together", "humanity"],
    "peace": ["peace", "harmony", "kindness"],
    "local": ["local", "community", "action"],
    "mental": ["mental health", "self-care", "judgment", "healing", "okay"]
}

all_responses = [resp for cat in responses.values() for resp in cat]

# Chat functions (for igc.html)
def display_message(message, sender):
    chat_box = document.getElementById("chatBox")
    if chat_box:
        message_div = document.createElement("div")
        message_div.classList.add("message", sender)
        message_div.textContent = message
        chat_box.appendChild(message_div)
        chat_box.scrollTop = chat_box.scrollHeight

def get_response(user_input, category_filter):
    user_input = user_input.lower()
    if category_filter == "all":
        applicable_responses = all_responses
    else:
        applicable_responses = responses.get(category_filter, all_responses)
    for category, key_list in keywords.items():
        if any(key in user_input for key in key_list):
            if category_filter == "all" or category_filter == category:
                return random.choice(responses[category])
    return random.choice(applicable_responses) if applicable_responses else "Ask me about climate, equality, or mental health!"

def send_message(event):
    user_input_elem = document.getElementById("userInput")
    if user_input_elem and user_input_elem.value.strip():
        user_input = user_input_elem.value.strip()
        display_message(user_input, "user")
        user_input_elem.value = ""
        category_filter = document.getElementById("categoryFilter").value
        response = get_response(user_input, category_filter)
        display_message(response, "ai")

def clear_chat(event):
    chat_box = document.getElementById("chatBox")
    if chat_box:
        chat_box.innerHTML = ""

def save_chat(event):
    chat_box = document.getElementById("chatBox")
    if chat_box:
        chat_content = chat_box.textContent
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"brainstorm_chat_{timestamp}.txt"
        blob = Blob.new([chat_content], {"type": "text/plain"})
        url = URL.createObjectURL(blob)
        link = document.createElement("a")
        link.href = url
        link.download = filename
        link.click()
        URL.revokeObjectURL(url)
        display_message(f"Chat saved as {filename}", "ai")

# Game functions (for game.html)
def display_game_output(output):
    game_area = document.getElementById("gameArea")
    if game_area:
        output_div = document.createElement("div")
        output_div.classList.add("game-output")
        output_div.textContent = output
        game_area.appendChild(output_div)
        game_area.scrollTop = game_area.scrollHeight

def play_game(event):
    game_input_elem = document.getElementById("gameInput")
    if game_input_elem and game_input_elem.value.strip():
        user_input = game_input_elem.value.strip()
        game_type = document.getElementById("gameSelect").value
        display_game_output(f"Your input: {user_input}")
        if game_type == "wordAssociation":
            words = user_input.split()
            response = f"Associated idea: {random.choice(words)} + {random.choice(['hope', 'action', 'nature', 'unity'])}"
        elif game_type == "ideaChain":
            response = f"Next in chain: {user_input} → {random.choice(['community', 'innovation', 'sustainability', 'peace'])}"
        elif game_type == "whatIf":
            response = f"What if {user_input} led to {random.choice(['global peace', 'clean energy', 'equal opportunities'])}?"
        display_game_output(response)
        game_input_elem.value = ""

def clear_game(event):
    game_area = document.getElementById("gameArea")
    if game_area:
        game_area.innerHTML = ""

# Theme toggle (for all pages)
def toggle_theme(event):
    body = document.querySelector("body")
    theme_toggle = document.getElementById("themeToggle")
    if body and theme_toggle:
        body.classList.toggle("dark-theme")
        if "dark-theme" in body.classList:
            window.localStorage.setItem("theme", "dark")
            theme_toggle.textContent = "Light Mode"
        else:
            window.localStorage.setItem("theme", "light")
            theme_toggle.textContent = "Dark Mode"

# Initialize theme (for all pages)
saved_theme = window.localStorage.getItem("theme")
theme_toggle = document.getElementById("themeToggle")
if theme_toggle:
    if saved_theme == "dark":
        document.querySelector("body").classList.add("dark-theme")
        theme_toggle.textContent = "Light Mode"
    else:
        theme_toggle.textContent = "Dark Mode"

# Bind events based on page content
def bind_events():
    # Theme toggle (all pages)
    theme_toggle = document.getElementById("themeToggle")
    if theme_toggle:
        theme_toggle.onclick = toggle_theme

    # IGC page events
    send_button = document.getElementById("sendButton")
    if send_button:
        send_button.onclick = send_message
    
    clear_chat_button = document.getElementById("clearChat")
    if clear_chat_button:
        clear_chat_button.onclick = clear_chat
    
    save_chat_button = document.getElementById("saveChat")
    if save_chat_button:
        save_chat_button.onclick = save_chat
    
    user_input = document.getElementById("userInput")
    if user_input:
        user_input.onkeypress = lambda e: send_message(e) if e.key == "Enter" else None

    # Game page events
    play_game_button = document.getElementById("playGame")
    if play_game_button:
        play_game_button.onclick = play_game
    
    clear_game_button = document.getElementById("clearGame")
    if clear_game_button:
        clear_game_button.onclick = clear_game
    
    game_input = document.getElementById("gameInput")
    if game_input:
        game_input.onkeypress = lambda e: play_game(e) if e.key == "Enter" else None

bind_events()