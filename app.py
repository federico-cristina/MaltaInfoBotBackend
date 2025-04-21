from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)  # 🔓 Permette richieste dal frontend React

# Setup Gemini
client = genai.Client(api_key="AIzaSyA_OTqUtUcqBQ788Ru3rRn0rZGxxZyirR8")

chat = client.chats.create(model="gemini-2.0-flash")

with open("promptMaltaInfoBot.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

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
