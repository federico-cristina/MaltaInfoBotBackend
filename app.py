from flask import Flask, request, jsonify
from flask_cors import CORS
from google import generativeai as genai
from dotenv import load_dotenv
from os import getenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configura l'API key
genai.configure(api_key=getenv("GEMINI_API_KEY"))

# Istanzia il modello
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

# Avvia la chat con un prompt iniziale
with open("promptMaltaInfoBot.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

chat = model.start_chat(history=[])
chat.send_message(system_prompt)

@app.route("/api/chat", methods=["POST"])
def chat_with_gemini():
    data = request.get_json()
    user_input = data.get("message")

    if not user_input:
        return jsonify({"error": "Missing message"}), 400

    response = chat.send_message(user_input)
    return jsonify({"response": response.text})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
