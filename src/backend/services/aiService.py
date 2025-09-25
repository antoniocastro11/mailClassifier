
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

emails = [
    "Quero saber o status da minha requisição",
    "Poderia me atualizar sobre meu pedido?",
    "Estou com problema no sistema",
    "Não consigo acessar minha conta",
    "Gostaria de uma cotação de preços",
    "Preciso de informações comerciais",
    "Feliz Natal para todos",
    "Muito obrigado pelo atendimento",
    "Bom dia, como vocês estão?"
]
labels = [
    "Produtivo", "Produtivo",   
    "Produtivo", "Produtivo",    
    "Produtivo", "Produtivo",    
    "Improdutivo", "Improdutivo", "Improdutivo"
]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(emails)
clf = MultinomialNB()
clf.fit(X, labels)

def classify_and_answer(email_text: str):
    X_new = vectorizer.transform([email_text])
    categoria = clf.predict(X_new)[0]

    if categoria == "Produtivo":
        resposta = "Recebemos sua solicitação e vamos dar andamento em breve."
    else:
        resposta = "Obrigado pela sua mensagem! Desejamos um ótimo dia."

    return {"categoria": categoria, "resposta": resposta}
