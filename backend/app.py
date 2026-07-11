from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from dotenv import load_dotenv
import os
import traceback
from collections import deque
from utils.prompt_builder import prompt_builder
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
# Global Chat History (Automated max length of 10 items)
# ============================================================

chat_history = deque(maxlen=10)


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
        # Route the query & Search Knowledge Base (With Second Chance Fallback)
        # ============================================================

        route = query_router.detect(message)
        
        category = route["category"]
        confidence = route["confidence"]
        matched_keywords = route["matched_keywords"]

        print("=" * 80)
        print("CATEGORY :", category)
        print("CONFIDENCE :", confidence)
        print("MATCHED :", matched_keywords)
        print("=" * 80)

        search_results = knowledge_search.search(
            query=message,
            category=category
        )
        
        # Second Chance: If nothing useful is found, search everywhere (general)
        if not search_results and category != "general":
            search_results = knowledge_search.search(
                query=message,
                category="general"
            )

        # Empty search mitigation
        if not search_results:
            return jsonify({
                "reply":
                (
                    "I couldn't find information related to your question "
                    "in the LBS knowledge base.\n\n"
                    "You can ask me about:\n"
                    "• Courses\n"
                    "• Admissions\n"
                    "• Faculty\n"
                    "• Branches\n"
                    "• Contact details\n"
                    "• Placement support\n"
                    "• Institute information"
                )
            })

        # ============================================================
        # Cleaned Debug Logs
        # ============================================================

        print("=" * 80)
        print("RESULTS  :", len(search_results))

        for r in search_results:
            print(f"{r['section']} -> {r['title']}")

        print("=" * 80)

        # ============================================================
        # Build Context
        # ============================================================
      
        context = context_builder.build(search_results)

        # ============================================================
        # Store User Message & Setup Window
        # ============================================================

        chat_history.append(f"User: {message}")
        
        # Creates history string out of the last 6 operations inside deque
        current_history_list = list(chat_history)
        conversation = "\n".join(current_history_list[-6:])

        # ============================================================
        # Prompt Construction & Gemini Generation
        # ============================================================

        prompt = prompt_builder.build(
            question=message,
            context=context,
            conversation=conversation
        )

        options = genai.types.GenerationConfig(temperature=0.7)
        response = model.generate_content(prompt, generation_config=options)
        reply = response.text.strip()

        # ============================================================
        # Save Assistant Reply (Deque manages the max size of 10)
        # ============================================================

        chat_history.append(f"Assistant: {reply}")

        print("=" * 60)
        print("Assistant:", reply)
        print("=" * 60)

        return jsonify({
            "reply": reply
        })
        
    except Exception as e:

        # ============================================================
        # Enhanced Error Logging via Traceback
        # ============================================================
        print("=" * 60)
        print("ERROR OCCURRED")
        traceback.print_exc()
        print("=" * 60)

        return jsonify({
            "error": "Sorry, something went wrong while processing your request. Please try again later or contact LBSTI at +91 8273817564."
        }), 500


# ============================================================
# Run Application
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)