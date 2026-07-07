from utils.query_router import query_router
from utils.knowledge_search import knowledge_search
from utils.context_builder import context_builder
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables (Local fallback only)
load_dotenv()

# Get Gemini API key directly from Vercel's Environment Settings
api_key = os.getenv("GEMINI_API_KEY")
print("API Key:", os.getenv("GEMINI_API_KEY"))
print("Configured API Key:", api_key)
# Configure Gemini
genai.configure(api_key=api_key)

# Create Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

# Initialize Flask App
app = Flask(__name__)

# EXPLICITLY assign for Vercel serverless targeting 
app = app 

# Global chat history tracking
chat_history = []



@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({
        "status": "ok"
    })

@app.route("/suggestions")
def suggestions():
    return jsonify([
        "What courses are available?",
        "What is the contact number?",
        "Where is the institute located?",
        "What is the email address?",
        "How can I take admission?"
    ])

@app.route("/clear-history", methods=["POST"])
def clear_history():
    global chat_history
    chat_history = []
    return jsonify({
        "message": "Conversation history cleared."
    })


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
        print("User Message:", message)

        # Detect category
        category = query_router.detect(message)
        print("Detected Category:", category)

        # Search knowledge base
        search_results = knowledge_search.search(message)

        # Build context
        context = context_builder.build(search_results)

        # Save conversation
        chat_history.append(f"User: {message}")
        conversation_context = "\n".join(chat_history[-6:])

        prompt = f"""
You are the official AI Assistant of Lal Bahadur Shastri Training Institute (LBSTI), Pithoragarh.

Relevant Institute Information:

{context}

Previous Conversation:

{conversation_context}

Current User Question:

{message}

Instructions:

1. Answer institute-related questions ONLY using the information provided above.

2. If the answer is not available in the knowledge base, politely say:
"I couldn't find that information in the institute knowledge base. Please contact the institute for further assistance."

3. If the question is unrelated to the institute, answer normally.

4. Keep responses friendly, professional and concise.

Assistant:
"""

        response = model.generate_content(prompt)
        reply = response.text

        chat_history.append(f"Assistant: {reply}")

        return jsonify({
            "reply": reply
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({
            "error": "For more information, please contact +91 8273817562."
        }), 500
    
if __name__ == "__main__":
    app.run(debug=True)