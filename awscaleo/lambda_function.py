import json
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import DynamoDBChatMessageHistory

# Define o template do prompt do chat
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Você é um assistente útil."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

# Define a cadeia de execução principal
chain = prompt | ChatOpenAI()

# Configura a cadeia com histórico de mensagens
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: DynamoDBChatMessageHistory(table_name="memory_chatbot",
                                                  primary_key_name='id',
                                                  session_id=session_id,
                                                  ttl=86400,
                                                  ttl_key_name='ExpirationTime'),
    input_messages_key="question",
    history_messages_key="history",
)


def lambda_handler(event, context):
    # Extrai o question e session_id do corpo da solicitação
    question = event['question']
    session_id = event['session_id']
    
    # Configura o session_id na cadeia
    config = {"configurable": {"session_id": session_id}}
    
    # Invoca a cadeia de execução com o question e session_id
    response = chain_with_history.invoke({"question": question}, config=config)
    
    # Retorna o conteúdo da resposta
    return {
        'statusCode': 200,
        'body': json.dumps({'response': response.content})
    }