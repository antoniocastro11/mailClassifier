from openai import OpenAI
from config import OPENAPI_KEY

client = OpenAI(api_key=OPENAPI_KEY)

def classify_and_answer(emailText: str):
    prompt = f"""
    Você é um assistente que classifica os emails recebidos em uma empresa.
    Existem duas categorias possíveis: 
    1. Produtivo: requer ação ou resposta específica. Exemplos:
    2. Improdutivo: não requer ações imediatas: Exemplos:

    Tarefa:
    1. Classifique o seguinte email como "Produtivo" ou "Improdutivo".
    2. Sugira uma resposta automática curta e adequada

    email: {emailText}
    Responda em JSON, assim:
    {{
        "categoria": "...",
        "resposta": "..."
    }} 
    """
      response = client.chat.completions.create(
        model="gpt-4o-mini",  # mais rápido e barato
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    raw_output = response.choices[0].message.content

    import json
    try:
        result= json.loads(raw_output)
    except:
        result = {"categoria": "indefinido",
                  "resposta": raw_output}
    return result
