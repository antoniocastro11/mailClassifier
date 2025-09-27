from flask import Flask, request, jsonify
from flask_cors import CORS
from services.aiService import classify_and_answer
from utils.fileReader import extract_text_from_file

app = Flask(__name__)
CORS(app)

@app.route("/classify", methods=["POST"])
def classify():
    email_text = ""

    if "file" in request.files:
        file = request.files["file"]
        try:
            email_text = extract_text_from_file(file)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    elif "email" in request.form:
        email_text = request.form["email"]
    elif request.is_json and "email" in request.json:
        email_text = request.json["email"]

    if not email_text.strip():
        return jsonify({"error": "Nenhum conteúdo de email fornecido"}), 400

    categoria, resposta = classify_and_answer(email_text)
    return jsonify({"categoria": categoria, "resposta": resposta})
