// BANCO DE PREGUNTAS (Estructura Original)
const preguntas = [
    {
        texto: "¿Cuál debería ser la prioridad económica del país?",
        opciones: [
            { texto: "Libre mercado y reducción de impuestos", scores: { Abelardo: 0, Cepeda: 0, Paloma: 10, Fajardo: 5 } },
            { texto: "Intervención estatal y reforma agraria", scores: { Abelardo: 0, Cepeda: 10, Paloma: 0, Fajardo: 3 } },
            { texto: "Educación e innovación tecnológica", scores: { Abelardo: 0, Cepeda: 5, Paloma: 3, Fajardo: 10 } },
            { texto: "Seguridad y control institucional", scores: { Abelardo: 10, Cepeda: 0, Paloma: 8, Fajardo: 2 } }
        ]
    },
    {
        texto: "¿Cómo abordar el conflicto armado y la seguridad?",
        opciones: [
            { texto: "Mano dura y fortalecimiento militar", scores: { Abelardo: 10, Cepeda: 0, Paloma: 10, Fajardo: 2 } },
            { texto: "Diálogos de paz y justicia social", scores: { Abelardo: 0, Cepeda: 10, Paloma: 0, Fajardo: 6 } },
            { texto: "Cumplimiento estricto de acuerdos previos", scores: { Abelardo: 0, Cepeda: 8, Paloma: 2, Fajardo: 10 } }
        ]
    },
    {
        texto: "¿Qué modelo de salud prefieres?",
        opciones: [
            { texto: "Público y preventivo al 100%", scores: { Abelardo: 0, Cepeda: 10, Paloma: 0, Fajardo: 4 } },
            { texto: "Mixto con fuerte regulación", scores: { Abelardo: 0, Cepeda: 5, Paloma: 3, Fajardo: 10 } },
            { texto: "Privado basado en EPS", scores: { Abelardo: 10, Cepeda: 0, Paloma: 10, Fajardo: 2 } }
        ]
    }
];

// ESTADO DE LA APLICACIÓN
let currentIndex = 0;
let respuestasUsuario = {}; // { indexPregunta: indexOpcion }
let chartInstance = null;

// INICIALIZACIÓN Y PERSISTENCIA
document.addEventListener("DOMContentLoaded", () => {
    const saved = localStorage.getItem("voto_informado_respuestas");
    if (saved) {
        respuestasUsuario = JSON.parse(saved);
        if (Object.keys(respuestasUsuario).length === preguntas.length) {
            mostrarResultados();
        } else {
            currentIndex = Math.max(...Object.keys(respuestasUsuario).map(Number)) + 1 || 0;
            if (currentIndex >= preguntas.length) currentIndex = 0;
            iniciarTest(true);
        }
    }
});

function iniciarTest(fromSave = false) {
    document.getElementById("screen-start").classList.add("hidden");
    document.getElementById("screen-results").classList.add("hidden");
    document.getElementById("screen-test").classList.remove("hidden");
    if (!fromSave) {
        respuestasUsuario = {};
        currentIndex = 0;
        localStorage.removeItem("voto_informado_respuestas");
    }
    renderPregunta();
}

// LÓGICA DEL TEST
function renderPregunta() {
    const p = preguntas[currentIndex];
    document.getElementById("progress-text").innerText = `Pregunta ${currentIndex + 1} de ${preguntas.length}`;
    document.getElementById("question-text").innerText = p.texto;
    
    const container = document.getElementById("options-container");
    container.innerHTML = "";
    
    p.opciones.forEach((opc, i) => {
        const btn = document.createElement("button");
        btn.className = "option-btn";
        if (respuestasUsuario[currentIndex] === i) btn.classList.add("selected");
        btn.innerText = opc.texto;
        btn.onclick = () => seleccionarOpcion(i);
        container.appendChild(btn);
    });

    document.getElementById("btn-prev").disabled = currentIndex === 0;
    
    const isAnswered = respuestasUsuario.hasOwnProperty(currentIndex);
    const btnNext = document.getElementById("btn-next");
    btnNext.innerText = currentIndex === preguntas.length - 1 ? "Ver Resultados" : "Siguiente";
    btnNext.disabled = !isAnswered;
}

function seleccionarOpcion(indexOpcion) {
    respuestasUsuario[currentIndex] = indexOpcion;
    localStorage.setItem("voto_informado_respuestas", JSON.stringify(respuestasUsuario));
    
    // Indicador visual de guardado
    const indicator = document.getElementById("saved-indicator");
    indicator.classList.remove("hidden");
    setTimeout(() => indicator.classList.add("hidden"), 1000);
    
    renderPregunta();
}

function preguntaAnterior() {
    if (currentIndex > 0) { currentIndex--; renderPregunta(); }
}

function siguientePregunta() {
    if (currentIndex < preguntas.length - 1) {
        currentIndex++; renderPregunta();
    } else {
        mostrarResultados();
    }
}

// CÁLCULO Y DASHBOARD
function calcularAfinidad() {
    const totales = { Abelardo: 0, Cepeda: 0, Paloma: 0, Fajardo: 0 };
    const maximosPosibles = { Abelardo: 0, Cepeda: 0, Paloma: 0, Fajardo: 0 };

    for (let i = 0; i < preguntas.length; i++) {
        // Encontrar el puntaje máximo posible por pregunta para normalizar
        let maxAb = 0, maxCe = 0, maxPa = 0, maxFa = 0;
        preguntas[i].opciones.forEach(opc => {
            if(opc.scores.Abelardo > maxAb) maxAb = opc.scores.Abelardo;
            if(opc.scores.Cepeda > maxCe) maxCe = opc.scores.Cepeda;
            if(opc.scores.Paloma > maxPa) maxPa = opc.scores.Paloma;
            if(opc.scores.Fajardo > maxFa) maxFa = opc.scores.Fajardo;
        });
        maximosPosibles.Abelardo += maxAb; maximosPosibles.Cepeda += maxCe;
        maximosPosibles.Paloma += maxPa; maximosPosibles.Fajardo += maxFa;

        // Sumar selección del usuario
        if (respuestasUsuario[i] !== undefined) {
            const seleccion = preguntas[i].opciones[respuestasUsuario[i]].scores;
            totales.Abelardo += seleccion.Abelardo;
            totales.Cepeda += seleccion.Cepeda;
            totales.Paloma += seleccion.Paloma;
            totales.Fajardo += seleccion.Fajardo;
        }
    }

    // Calcular porcentajes
    const resultados = [];
    for (const [candidato, pts] of Object.entries(totales)) {
        const porcentaje = maximosPosibles[candidato] > 0 ? Math.round((pts / maximosPosibles[candidato]) * 100) : 0;
        resultados.push({ candidato, porcentaje });
    }
    
    return resultados.sort((a, b) => b.porcentaje - a.porcentaje);
}

function mostrarResultados() {
    document.getElementById("screen-test").classList.add("hidden");
    document.getElementById("screen-results").classList.remove("hidden");
    
    const ranking = calcularAfinidad();
    
    // 1. Renderizar Ranking
    const list = document.getElementById("ranking-container");
    list.innerHTML = "";
    ranking.forEach((r, i) => {
        const li = document.createElement("li");
        li.innerHTML = `<strong>#${i+1} ${r.candidato}</strong>: ${r.porcentaje}% de afinidad`;
        list.appendChild(li);
    });

    // 2. Renderizar Radar Chart
    const ctx = document.getElementById('radarChart').getContext('2d');
    if (chartInstance) chartInstance.destroy();
    chartInstance = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ranking.map(r => r.candidato),
            datasets: [{
                label: 'Tu Perfil Ideológico',
                data: ranking.map(r => r.porcentaje),
                backgroundColor: 'rgba(59, 130, 246, 0.2)',
                borderColor: 'rgba(59, 130, 246, 1)',
                borderWidth: 2,
                pointBackgroundColor: 'rgba(59, 130, 246, 1)'
            }]
        },
        options: { scales: { r: { beginAtZero: true, max: 100 } } }
    });
}

function reiniciarTest() {
    if(confirm("¿Seguro que quieres borrar tus resultados y empezar de cero?")) {
        localStorage.removeItem("voto_informado_respuestas");
        document.getElementById("chat-box").innerHTML = '<div class="msg bot">¡Hola! He analizado tus resultados. ¿Tienes alguna pregunta sobre tu afinidad con estos candidatos o sus propuestas?</div>';
        iniciarTest();
    }
}

// LÓGICA DEL CHATBOT GEMINI
function handleEnter(e) { if(e.key === 'Enter') enviarMensajeIA(); }

async function enviarMensajeIA() {
    const input = document.getElementById("chat-input-text");
    const btn = document.getElementById("chat-send-btn");
    const box = document.getElementById("chat-box");
    const msg = input.value.trim();
    
    if (!msg) return;

    // UI: Mensaje Usuario
    input.value = "";
    input.disabled = true;
    btn.disabled = true;
    box.innerHTML += `<div class="msg user">${msg}</div>`;
    
    // UI: Loading
    const loadingId = "load-" + Date.now();
    box.innerHTML += `<div class="msg loading" id="${loadingId}">Gemini procesando...</div>`;
    box.scrollTop = box.scrollHeight;

    // Obtener contexto real del dashboard
    const rankingData = calcularAfinidad();
    const contexto = {
        resultado_principal: rankingData[0].candidato,
        ranking: rankingData.map(r => `${r.candidato}: ${r.porcentaje}%`)
    };

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: msg, context: contexto })
        });
        
        document.getElementById(loadingId).remove();
        
        if (!response.ok) throw new Error("Error en el servidor de Render");
        
        const data = await response.json();
        const reply = data.reply || data.error;
        box.innerHTML += `<div class="msg bot">${reply}</div>`;
    } catch (error) {
        document.getElementById(loadingId).remove();
        box.innerHTML += `<div class="msg bot" style="color:red;">Error de conexión. Verifica la API Key en Render.</div>`;
    } finally {
        input.disabled = false;
        btn.disabled = false;
        input.focus();
        box.scrollTop = box.scrollHeight; // Scroll Automático garantizado
    }
}

// EXPORTACIÓN A PDF (jsPDF)
function exportarPDF() {
    window.jsPDF = window.jspdf.jsPDF;
    const doc = new jsPDF();
    const ranking = calcularAfinidad();
    
    doc.setFontSize(22);
    doc.text("Resultados - Voto Informado 2.0", 20, 20);
    
    doc.setFontSize(14);
    doc.text("Tu ranking de afinidad:", 20, 40);
    
    let y = 50;
    ranking.forEach((r, i) => {
        doc.text(`${i+1}. ${r.candidato} - ${r.porcentaje}%`, 30, y);
        y += 10;
    });
    
    doc.setFontSize(10);
    doc.text("Generado por Asistente Electoral IA", 20, 280);
    doc.save("Resultados_Voto_Informado.pdf");
}
