from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from dotenv import load_dotenv
import os

from utils.query_router import query_router
from utils.knowledge_search import knowledge_search
from utils.context_builder import context_builder


# ============================================================
# Load Environment Variables
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found.")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")


# ============================================================
# Flask App
# ============================================================

app = Flask(__name__)

# Required for Vercel
app = app


# ============================================================
# Global Chat History
# ============================================================

chat_history = []


# ============================================================
# Home Route
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# Health Check
# ============================================================

@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "message": "LBSTI AI Assistant is running successfully."
    })


# ============================================================
# Suggestion Chips
# ============================================================

@app.route("/suggestions")
def suggestions():

    suggestion_list = [
        "What courses are available?",
        "Tell me about Python course",
        "How can I take admission?",
        "What is the fee structure?",
        "Where is the institute located?",
        "What is the contact number?",
        "Who are the faculty members?",
        "Do you provide placement assistance?",
        "Tell me about LBSTI",
        "Do you have eBooks?"
    ]

    return jsonify(suggestion_list)


# ============================================================
# Clear Chat History
# ============================================================

@app.route("/clear-history", methods=["POST"])
def clear_history():

    global chat_history

    chat_history.clear()

    return jsonify({
        "success": True,
        "message": "Conversation history cleared successfully."
    })


# ============================================================
# Chat Endpoint
# ============================================================

@app.route("/chat", methods=["POST"])
def chat():

    global chat_history

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Invalid JSON request."
        }), 400

    message = data.get("message", "").strip()

    if not message:
        return jsonify({
            "error": "Message cannot be empty."
        }), 400

    try:

        print("=" * 60)
        print("User:", message)
                # ============================================================
        # Route the query
        # ============================================================

        category = query_router.detect(message)

        print("Detected Category:", category)

        # ============================================================
        # Search Knowledge Base
        # ============================================================

        search_results = knowledge_search.search(message)

        print("Search Results Found:", len(search_results))

        # ============================================================
        # Build Context
        # ============================================================

        context = context_builder.build(search_results)

        # ============================================================
        # Store User Message
        # ============================================================

        chat_history.append(f"User: {message}")

        # Keep only last 10 messages
        if len(chat_history) > 10:
            chat_history = chat_history[-10:]

        conversation_context = "\n".join(chat_history)

        # ============================================================
        # Prompt for Gemini
        # ============================================================

        prompt = f"""
You are the official AI Assistant of Lal Bahadur Shastri Training Institute (LBSTI), Pithoragarh.

You help students with institute-related questions.

==========================================================
RELEVANT KNOWLEDGE
==========================================================

{context}

==========================================================
PREVIOUS CONVERSATION
==========================================================

{conversation_context}

==========================================================
CURRENT USER QUESTION
==========================================================

{message}

==========================================================
RULES
==========================================================

1. Answer institute-related questions ONLY using the knowledge provided above.

2. If the requested institute information is missing from the knowledge base,
reply politely:

"I couldn't find that information in the institute knowledge base. Please contact the institute for further assistance."

3. If the user's question is NOT related to LBSTI, answer normally using your general knowledge.

4. Never invent institute information.

5. Keep answers clear, professional and concise.

Assistant:
"""

        # ============================================================
        # Gemini Response
        # ============================================================

        response = model.generate_content(prompt)

        reply = response.text.strip()

        # ============================================================
        # Save Assistant Reply
        # ============================================================

        chat_history.append(f"Assistant: {reply}")

        if len(chat_history) > 10:
            chat_history = chat_history[-10:]

        print("=" * 60)
        print("Assistant:", reply)
        print("=" * 60)

        return jsonify({
            "reply": reply
        })
    except Exception as e:

        print("=" * 60)
        print("ERROR OCCURRED")
        print(e)
        print("=" * 60)

        return jsonify({
            "error": "Sorry, something went wrong while processing your request. Please try again later or contact LBSTI at +91 8273817564."
        }), 500


# ============================================================
# Run Application
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)