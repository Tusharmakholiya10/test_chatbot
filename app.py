from flask import Flask, request, jsonify, render_template
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

# Global chat history tracking
chat_history = []

LBS_CONTEXT = """
You are the official AI Assistant of Lal Bahadur Shastri Training Institute (LBSTI), Pithoragarh.

Institute Information:
- Name: Lal Bahadur Shastri Training Institute, Pithoragarh
- Address: Link Road, Opposite Pizza Slice, Pithoragarh - 262501
- Phone: +91 8273817564
- Email: lbspth@gmail.com

Courses Offered:
- Diploma in Information Technology (Duration: 1 year)
- Diploma in Web Technology (Duration: 1 year 6 months)
- Tally Prime (Duration: 3 months)

If the question is related to the institute, answer using this information.
If the question is unrelated to the institute, answer using general knowledge.
"""

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
        lower_message = message.lower()
        print("User Message:", lower_message)

        # -----------------------------
        # Direct answers for LBS FAQs
        # -----------------------------

        if "course" in lower_message:
            print("COURSE CONDITION TRIGGERED")

            reply = (
                "LBSTI currently offers:\n\n"
                "• Diploma in Information Technology (1 year)\n"
                "• Diploma in Web Technology (1 year 6 months)\n"
                "• Tally Prime (3 months)\n\n"
                "The institute also offers multiple computer and technology skill development courses."
            )

        elif any(word in lower_message for word in [
    "contact",
    "phone",
    "mobile",
    "number"
]):
            print("CONTACT CONDITION TRIGGERED")

            reply = (
        "You can contact Lal Bahadur Shastri Training Institute "
        "at +91 8273817564."
    )

        elif "email" in lower_message:
            reply = (
                "You can reach the institute at: lbspth@gmail.com"
            )

        elif any(word in lower_message for word in [
            "address",
            "location",
            "where"
        ]):
            reply = (
                "Lal Bahadur Shastri Training Institute is located at:\n"
                "Link Road, Opposite Pizza Slice,\n"
                "Pithoragarh - 262501."
            )

        else:
            # -----------------------------
            # Gemini for all other queries
            # -----------------------------

            chat_history.append(f"User: {message}")

            conversation_context = "\n".join(chat_history[-6:])

            prompt = f"""
{LBS_CONTEXT}

Previous Conversation:
{conversation_context}

Current User Question:
{message}

Instructions:
- Treat institute-related questions as being about LBSTI.
- Use the institute information provided above whenever applicable.
- For non-institute questions, answer normally using general knowledge.
- Keep answers concise and helpful.

Assistant Response:
"""

            response = model.generate_content(prompt)
            reply = response.text

        # Save assistant response
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

from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Essential for Vercel to find the app object
app = app 

@app.route('/')
def home():
    return render_template('index.html')

# ... rest of your chatbot routes ...

if __name__ == '__main__':
    app.run(debug=True)