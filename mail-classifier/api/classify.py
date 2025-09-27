from services.aiService import classify_and_answer
from utils.fileReader import extract_text_from_file
from flask import jsonify, request

def handler(request):
    email_text = ""

    if "file" in request.files:
        file = request.files["file"]
        email_text = extract_text_from_file(file)
    elif "email" in request.form:
        email_text = request.form["email"]
    elif request.is_json and "email" in request.json:
        email_text = request.json["email"]

    if not email_text.strip():
        return jsonify({"error": "Nenhum conteúdo de email fornecido"}), 400

    categoria, resposta = classify_and_answer(email_text)
    return jsonify({"categoria": categoria, "resposta": resposta})
