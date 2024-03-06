function generateSessionId() {
    // Gera um identificador único baseado na data/hora e em um número aleatório
    return 'sess-' + new Date().getTime().toString(36) + '-' + Math.random().toString(36).substr(2, 9);
}

const sessionId = generateSessionId();
displayMessage(`Sessão Iniciada: ${sessionId}` , 'bot-message');

async function sendMessage() {
    var inputElement = document.getElementById("userInput");
    var userInput = inputElement.value;
    if (userInput.trim() === '') return; // Não fazer nada se a entrada estiver vazia

    displayMessage(userInput, 'user-message'); // Mostra a mensagem do usuário

    // Chama a API para obter a resposta do bot
    try {
        const response = await fetch('https://h5xyawjq1l.execute-api.sa-east-1.amazonaws.com/chatbot_aws/simple_response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                session_id: sessionId,
                question: userInput
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        const body = JSON.parse(data.body); // Agora deserializa a string JSON do body para um objeto JavaScript
        const answer = body.response; // Extrai o campo 'response' do objeto body
        
        displayMessage(answer, 'bot-message'); // Exibe a resposta do bot
    } catch (error) {
        console.error('Erro ao chamar a API:', error);
        displayMessage('Desculpe, algo deu errado ao obter uma resposta.', 'bot-message');
    }

    inputElement.value = ''; // Limpa o campo de entrada
}

function displayMessage(message, className) {
    var chatContainer = document.getElementById("chat-container");
    var messageElement = document.createElement("div");
    messageElement.classList.add("message", className);
    messageElement.textContent = message; // Exibe a mensagem de texto
    chatContainer.appendChild(messageElement);
    chatContainer.scrollTop = chatContainer.scrollHeight; // Rola para a última mensagem
}

// Adicionando evento para enviar mensagem com a tecla Enter
document.getElementById("userInput").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault(); // Impede que o formulário seja enviado
        sendMessage(); // Chama a função sendMessage
    }
});
