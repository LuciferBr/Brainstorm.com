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

def switch_page(page_id):
    try:
        for section in document.querySelectorAll("section"):
            section.classList.remove("active")
        for btn in document.querySelectorAll("nav button"):
            btn.classList.remove("active")
        document.getElementById(page_id).classList.add("active")
        document.getElementById(f"{page_id}Btn").classList.add("active")
    except Exception as e:
        console.log(f"Error switching page: {str(e)}")

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
    else:
        console.log("Chat box not found")

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

# Initialize theme
saved_theme = window.localStorage.getItem("theme")
theme_toggle = document.getElementById("themeToggle")
if theme_toggle:
    if saved_theme == "dark":
        document.querySelector("body").classList.add("dark-theme")
        theme_toggle.textContent = "Light Mode"
    else:
        theme_toggle.textContent = "Dark Mode"

def bind_events():
    elements = {
        "homeBtn": lambda e: switch_page("home"),
        "aboutBtn": lambda e: switch_page("about"),
        "igcBtn": lambda e: switch_page("igc"),
        "plansBtn": lambda e: switch_page("plans"),
        "gameBtn": lambda e: switch_page("game"),
        "themeToggle": toggle_theme,
        "sendButton": send_message,
        "clearChat": clear_chat,
        "saveChat": save_chat,
        "playGame": play_game,
        "clearGame": clear_game
    }
    for element_id, func in elements.items():
        elem = document.getElementById(element_id)
        if elem:
            elem.onclick = func
        else:
            console.log(f"Element {element_id} not found")

    user_input = document.getElementById("userInput")
    if user_input:
        user_input.onkeypress = lambda e: send_message(e) if e.key == "Enter" else None

    game_input = document.getElementById("gameInput")
    if game_input:
        game_input.onkeypress = lambda e: play_game(e) if e.key == "Enter" else None

bind_events()