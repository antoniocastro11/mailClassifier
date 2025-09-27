# backend/utils/fileReader.py
import io
from PyPDF2 import PdfReader

def extract_text_from_file(file):
    filename = file.filename.lower()

    if filename.endswith(".txt"):
        return file.read().decode("utf-8", errors="ignore").strip()

    elif filename.endswith(".pdf"):
        text = ""
        try:
            file.stream.seek(0)
            pdf_reader = PdfReader(file.stream)
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
        except Exception as e:
            print(f"Erro ao ler PDF: {e}")
            return ""
        return text.strip()

    else:
        raise ValueError("Formato de arquivo não suportado. Use .txt ou .pdf.")
