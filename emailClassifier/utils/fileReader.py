import io
from PyPDF2 import PdfReader

def extract_text_from_file(file):
    filename = file.filename.lower()

    if filename.endswith(".txt"):
        text = file.read().decode("utf-8", errors="ignore").strip()

    elif filename.endswith(".pdf"):
        text = ""
        try:
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
        except Exception as e:
            print(f"Erro ao ler PDF: {e}")
            return ""
        text = " ".join(text.split())

    else:
        raise ValueError("Formato de arquivo não suportado. Use .txt ou .pdf.")
    return text
