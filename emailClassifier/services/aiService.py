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
except:
    nltk.download("stopwords", quiet=True)

try:
    RSLPStemmer()
except:
    nltk.download("rslp", quiet=True)

stopwords_pt = set(stopwords.words("portuguese"))
stemmer = RSLPStemmer()

def normalize_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    txt = text.lower()
    txt = unicodedata.normalize("NFKD", txt).encode("ASCII", "ignore").decode("utf-8")
    txt = re.sub(r"[^a-z0-9\s]", " ", txt)
    tokens = [stemmer.stem(t) for t in txt.split() if t and t not in stopwords_pt]
    return " ".join(tokens)

KEYWORDS_PRODUTIVOS = [
    "pedido", "solicitacao", "fatura", "acesso",
    "relatorio", "pagamento", "suporte", "ticket",
    "conta", "cancelamento", "verificar", "atualizacao", "andamento"
]

KEYWORDS_IMPRODUTIVOS = [
    "feliz", "parabens", "obrigado", "sucesso",
    "bom dia", "atencao", "cumprimentar"
]

def keywordsClassify(text: str):
    text_norm = normalize_text(text)
    score_prod = sum(1 for kw in KEYWORDS_PRODUTIVOS if kw in text_norm)
    score_improd = sum(1 for kw in KEYWORDS_IMPRODUTIVOS if kw in text_norm)

    if score_prod > 0:
        return "Produtivo"
    elif score_improd > 0:
        return "Improdutivo"
    else:
        return "Indefinido"

train_emails = [
    # Produtivos
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
    "Gostaria de saber sobre o andamento do meu ticket",
    "Meu pedido ainda não chegou, podem verificar?",
    "Preciso atualizar meus dados cadastrais",
    "Solicito informações sobre a fatura",
    "Não recebi o retorno do pedido que fiz",
    # Improdutivos
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
    "Felicitações a todos",
    "Que todos tenham um ótimo dia",
    "Agradeço a ajuda anterior",
    "Tudo de bom para você",
    "Desejo sucesso em seus projetos"
]

train_labels = [
    "Produtivo","Produtivo","Produtivo","Produtivo","Produtivo",
    "Produtivo","Produtivo","Produtivo","Produtivo","Produtivo",
    "Produtivo","Produtivo","Produtivo","Produtivo","Produtivo",
    "Improdutivo","Improdutivo","Improdutivo","Improdutivo","Improdutivo",
    "Improdutivo","Improdutivo","Improdutivo","Improdutivo","Improdutivo",
    "Improdutivo","Improdutivo","Improdutivo","Improdutivo","Improdutivo"
]

preprocessor = FunctionTransformer(lambda docs: [normalize_text(d) for d in docs], validate=False)
vectorizer = TfidfVectorizer(ngram_range=(1,1)) 
clf = LogisticRegression(max_iter=2000, class_weight="balanced", random_state=42)

model = Pipeline([
    ("pre", preprocessor),
    ("tfidf", vectorizer),
    ("clf", clf)
])

model.fit(train_emails, train_labels)

def classify_and_answer(email_text: str, min_prob=0.6):
    if not isinstance(email_text, str) or not email_text.strip():
        return "Indefinido", "Conteúdo do email vazio."

    categoria = keywordsClassify(email_text)
    if categoria != "Indefinido":
        resposta = "Obrigado pelo contato! Recebemos sua solicitação." if categoria == "Produtivo" else "Agradecemos sua mensagem!"
        return categoria, resposta

    probas = model.predict_proba([email_text])[0]
    pred = model.predict([email_text])[0]
    if max(probas) < min_prob:
        return "Indefinido", "Não foi possível classificar com confiança suficiente."

    resposta = "Obrigado pelo seu contato! Recebemos sua solicitação e retornaremos em breve." if pred == "Produtivo" else "Agradecemos sua mensagem! Desejamos um ótimo dia."
    return pred, resposta
