import re
import unicodedata

import nltk
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import Pipeline

try:
    stopwords.words("portuguese")
except LookupError:
    nltk.download("stopwords", quiet=True)

try:
    RSLPStemmer()
except LookupError:
    nltk.download("rslp", quiet=True)

stopwords_pt = set(stopwords.words("portuguese"))
stemmer = RSLPStemmer()


def normalize_text(text: str) -> str:
    if not isinstance(text, str):
        return ""

    txt = text.lower()
    txt = unicodedata.normalize("NFKD", txt).encode("ASCII", "ignore").decode("utf-8")
    txt = re.sub(r"[^a-z0-9\s]", " ", txt)

    tokens = [t for t in txt.split() if t and t not in stopwords_pt]
    tokens = [stemmer.stem(t) for t in tokens]
    return " ".join(tokens)


train_emails = [
    # produtivos
    "Preciso de ajuda com minha conta",
    "Qual o status da minha solicitação?",
    "Segue em anexo o relatório solicitado",
    "Fiz um pagamento e não consta",
    "Não consigo acessar minha conta",
    "Erro ao processar pagamento",
    "Quando vou receber a fatura?",
    "Solicito cancelamento do meu pedido",
    "Meu acesso foi bloqueado, preciso de suporte",
    "Por favor confirmem o recebimento do arquivo",
    # improdutivos
    "Feliz Natal para toda a equipe!",
    "Feliz aniversário",
    "Parabéns pelo excelente trabalho",
    "Muito obrigado pelo suporte prestado",
    "Obrigado, equipe",
    "Bom dia, espero que todos estejam bem",
    "Apenas passando para cumprimentar",
    "Parabéns e sucesso sempre",
    "Agradeço a atenção",
    "Obrigado pelo retorno",
    "Felicitações a todos"
]

train_labels = [
    "Produtivo","Produtivo","Produtivo","Produtivo","Produtivo",
    "Produtivo","Produtivo","Produtivo","Produtivo","Produtivo",
    "Improdutivo","Improdutivo","Improdutivo","Improdutivo","Improdutivo",
    "Improdutivo","Improdutivo","Improdutivo","Improdutivo","Improdutivo","Improdutivo"
]


preprocessor = FunctionTransformer(lambda docs: [normalize_text(d) for d in docs], validate=False)
vectorizer = TfidfVectorizer(ngram_range=(1, 2))
clf = LogisticRegression(max_iter=2000, class_weight="balanced", random_state=42)

model = Pipeline([
    ("pre", preprocessor),
    ("tfidf", vectorizer),
    ("clf", clf)
])

model.fit(train_emails, train_labels)

def classify_and_answer(email_text: str):
    if not isinstance(email_text, str) or not email_text.strip():
        return "Indefinido", "Conteúdo do email vazio."

    pred = model.predict([email_text])[0]

    if pred == "Produtivo":
        resposta = "Obrigado pelo seu contato! Recebemos sua solicitação e retornaremos com uma atualização em breve."
    else:
        resposta = "Agradecemos sua mensagem! Desejamos um ótimo dia."

    return pred, resposta
