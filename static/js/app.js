// Variable global para guardar el contexto del test y enviárselo a Gemini
let userContext = {
    resultado_principal: "",
    porcentaje_afinidad: 0,
    ranking: [],
    respuestas_usuario: {}
};

// 1. Lógica para transicionar del Test a los Resultados
function finalizarTest() {
    // Aquí es donde normalmente calcularías los resultados reales de tu test.
    // Para asegurar que el chat funcione de inmediato, quemamos unos resultados de prueba.
    userContext.resultado_principal = "Fajardo"; 
    userContext.porcentaje_afinidad = 85;
    userContext.ranking = ["Fajardo: 85%", "Cepeda: 60%", "Paloma: 30%", "Abelardo: 10%"];

    // Actualizar UI
    document.getElementById('resultado-nombre').innerText = `Tu candidato ideal: ${userContext.resultado_principal}`;
    document.getElementById('resultado-porcentaje').innerText = `Afinidad: ${userContext.porcentaje_afinidad}%`;

    // Cambiar pantallas
    document.getElementById('test-section').classList.add('hidden');
    document.getElementById('results-section').classList.remove('hidden');
}

function reiniciarTest() {
    document.getElementById('test-section').classList.remove('hidden');
    document.getElementById('results-section').classList.add('hidden');
    document.getElementById('chat-messages').innerHTML = '<div class="message bot">¡Hola! He analizado tus resultados. ¿Tienes alguna pregunta sobre tu candidato afín o quieres comparar propuestas?</div>';
}

// 2. LÓGICA CRÍTICA DEL CHATBOT
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

async function sendMessage() {
    const inputField = document.getElementById('chat-input');
    const sendButton = document.getElementById('send-btn');
    const messagesContainer = document.getElementById('chat-messages');
    
    const message = inputField.value.trim();
    if (!message) return;

    // A. Mostrar mensaje del usuario
    appendMessage('user', message);
    inputField.value = '';
    
    // B. Preparar interfaz para cargar
    inputField.disabled = true;
    sendButton.disabled = true;
    
    const loadingId = 'loading-' + Date.now();
    appendLoading(loadingId);

    try {
        // C. Comunicación real con el backend (FastAPI -> Gemini)
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                context: userContext // Enviamos los resultados del test para que la IA sepa de qué hablar
            })
        });

        const data = await response.json();

        // Remover indicador de carga
        removeLoading(loadingId);

        // D. Mostrar respuesta de Gemini o Error
        if (response.ok && data.reply) {
            appendMessage('bot', data.reply);
        } else {
            appendMessage('bot', 'Error del sistema: ' + (data.error || 'No se pudo contactar a la IA.'));
        }
    } catch (error) {
        removeLoading(loadingId);
        appendMessage('bot', 'Error de conexión. Verifica tu internet o revisa los logs de Render.');
        console.error('Fetch error:', error);
    } finally {
        // E. Restaurar interfaz
        inputField.disabled = false;
        sendButton.disabled = false;
        inputField.focus();
    }
}

// Funciones de utilidad para el DOM del Chat
function appendMessage(sender, text) {
    const messagesContainer = document.getElementById('chat-messages');
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender);
    msgDiv.innerText = text;
    messagesContainer.appendChild(msgDiv);
    scrollToBottom();
}

function appendLoading(id) {
    const messagesContainer = document.getElementById('chat-messages');
    const loadingDiv = document.createElement('div');
    loadingDiv.id = id;
    loadingDiv.classList.add('loading');
    loadingDiv.innerText = 'Gemini está escribiendo...';
    messagesContainer.appendChild(loadingDiv);
    scrollToBottom();
}

function removeLoading(id) {
    const loadingDiv = document.getElementById(id);
    if (loadingDiv) loadingDiv.remove();
}

function scrollToBottom() {
    const messagesContainer = document.getElementById('chat-messages');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}
