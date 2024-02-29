import json
import openai
import os

# Define a função lambda handler
def lambda_handler(event, context):
    # Extrai a pergunta do corpo do evento (assumindo que a pergunta é enviada como um parâmetro JSON)
    question = json.loads(event['body'])['question']
    
    # Inicializa o cliente da OpenAI usando a chave de API armazenada em variáveis de ambiente
    client = openai.OpenAI(api_key=os.environ['OPENAI_API_KEY'])

    # Faz a chamada à API para obter uma resposta
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Você é um assistente útil projetado para gerar JSON."},
            {"role": "user", "content": question}
        ]
    )

    # Formata a resposta para JSON
    result = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': json.dumps({'answer': response.choices[0].message.content})
    }

    return result
