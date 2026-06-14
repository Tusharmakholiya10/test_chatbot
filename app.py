from flask import Flask, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)

# Create Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")

app = Flask(__name__)
chat_history = []               # (for history)

@app.route("/clear-history", methods=["POST"])
def clear_history():
    global chat_history

    chat_history = []

    return jsonify({
        "message": "Conversation history cleared."
    })


@app.route("/")
def home():
    return "Backend is running!"

@app.route("/health")
def health():
    return jsonify({
        "status": "ok"
    })

@app.route("/chat", methods=["POST"])
def chat():
    
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Invalid JSON request."
        }), 400

    message = data.get("message")

    if not message or not message.strip():
        return jsonify({
            "error": "Message cannot be empty."
    }), 400
    
    if not message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # 1. Everything that happens next MUST be indented inside the try block
        chat_history.append(f"User: {message}")

        # Build prompt using history
        prompt = "\n".join(chat_history)

        # Send to Gemini
        response = model.generate_content(prompt)
        reply = response.text

        # Save bot response
        chat_history.append(f"Assistant: {reply}")

        return jsonify({
            "reply": reply
        })

    except Exception as e:
        print("Error:", e)

    return jsonify({
        "error": "Sorry, something went wrong. Please try again later."
    }), 500

if __name__ == "__main__":
    app.run(debug=True)