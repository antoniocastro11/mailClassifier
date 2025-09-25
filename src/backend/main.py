from flask import Flask, request, jsonify
from flask_cors import CORS 
from services.aiService import classify_and_answer

app = Flask(__name__)
CORS(app)

@app.route('/classify', methods=['POST'])
def classify():
    data = request.json
    email_text = data.get('email', '')

    if not email_text.strip():
        return jsonify({"error": "email não fornecido"}), 400

    result = classify_and_answer(email_text)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)