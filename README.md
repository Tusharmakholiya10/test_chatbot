# AI Chatbot Backend using Flask and Gemini

## Features

- Gemini AI Integration
- Conversation History
- Error Handling
- Health Check Endpoint
- Clear History Endpoint

## Installation

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

## Run the Server

```bash
python app.py
```

## API Endpoints

### Health Check

GET /health

Response:

{
    "status": "ok"
}

### Chat

POST /chat

Request:

{
    "message": "Hello"
}

Response:

{
    "reply": "Gemini response"
}

### Clear History

POST /clear-history

Response:

{
    "message": "Conversation history cleared."
}