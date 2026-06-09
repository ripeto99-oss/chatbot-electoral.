// ==========================================
// 1. DATA CORE (Constantes Inmutables)
// ==========================================
const BRAND_DIMENSIONS = {
    1: { id: 'economia', name: 'Economía' },
    2: { id: 'social', name: 'Social' },
    3: { id: 'seguridad', name: 'Seguridad' },
    4: { id: 'futuro', name: 'Futuro' }
};

const CANDIDATES = {
    cepeda: {
        id: 'cepeda', name: 'Iván Cepeda', party: 'Pacto Histórico', color: '#6366f1', avatarText: 'IC', ideology: 'Izquierda Estructural',
        x_axis: -0.75, y_axis: 0.7, timeline: 'Senador. Co-arquitecto de procesos de paz.',
        answers: { 1:1, 2:0, 3:0, 4:1, 5:0, 6:0, 7:1, 8:1, 9:1, 10:1, 11:1, 12:1, 13:1, 14:0, 15:0, 16:0, 17:1, 18:0, 19:1, 20:0, 21:1, 22:1, 23:1, 24:0 }
    },
    espriella: {
        id: 'espriella', name: 'Abelardo de la Espriella', party: 'Defensores de la Patria', color: '#ef4444', avatarText: 'AE', ideology: 'Derecha Soberanista',
        x_axis: 0.85, y_axis: -0.8, timeline: 'Promotor de agenda punitiva y libre mercado.',
        answers: { 1:0, 2:1, 3:1, 4:0, 5:1, 6:1, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:1, 15:1, 16:1, 17:0, 18:1, 19:0, 20:1, 21:0, 22:0, 23:0, 24:1 }
    },
    valencia: {
        id: 'valencia', name: 'Paloma Valencia', party: 'Centro Democrático', color: '#3b82f6', avatarText: 'PV', ideology: 'Derecha Institucional',
        x_axis: 0.6, y_axis: -0.4, timeline: 'Representante histórica de seguridad democrática.',
        answers: { 1:0, 2:1, 3:1, 4:0, 5:1, 6:1, 7:0, 8:0, 9:1, 10:0, 11:1, 12:0, 13:0, 14:1, 15:1, 16:1, 17:0, 18:0, 19:0, 20:1, 21:0, 22:0, 23:0, 24:0 }
    },
    fajardo: {
        id: 'fajardo', name: 'Sergio Fajardo', party: 'Dignidad y Compromiso', color: '#f59e0b', avatarText: 'SF', ideology: 'Centro Pragmático',
        x_axis: -0.1, y_axis: 0.3, timeline: 'Académico enfocado en la educación.',
        answers: { 1:0, 2:0, 3:1, 4:0, 5:0, 6:1, 7:1, 8:1, 9:1, 10:1, 11:1, 12:0, 13:1, 14:0, 15:0, 16:0, 17:1, 18:0, 19:1, 20:0, 21:0, 22:1, 23:1, 24:0 }
    }
};

const BANK_QUESTIONS = [
    { id: 1, dimension: 1, topic: 'Tributaria', text: '¿Se debe tramitar una reforma tributaria enfocada en aumentar impuestos directos a los patrimonios más altos?' },
    { id: 2, dimension: 1, topic: 'Fracking', text: '¿Debe permitirse la exploración y explotación de hidrocarburos mediante fracturamiento hidráulico (Fracking)?' },
    { id: 3, dimension: 1, topic: 'Tarifas', text: '¿Debería el gobierno intervenir directamente los marcos de tarifas de los servicios públicos?' },
    { id: 4, dimension: 1, topic: 'Aranceles', text: '¿Es viable aumentar sustancialmente los aranceles a las importaciones de bienes agrícolas manufacturados?' },
    { id: 5, dimension: 1, topic: 'Regla Fiscal', text: '¿Se debe flexibilizar temporalmente la Regla Fiscal para apalancar inversión en infraestructura?' },
    { id: 6, dimension: 1, topic: 'TLCs', text: '¿Es imperativo renegociar unilateralmente los Tratados de Libre Comercio (TLC)?' },
    { id: 7, dimension: 2, topic: 'Salud', text: '¿Debe centralizarse la salud en una entidad estatal, eliminando la intermediación privada?' },
    { id: 8, dimension: 2, topic: 'Pensiones', text: '¿Se debe establecer un modelo donde las cotizaciones vayan obligatoriamente a Colpensiones?' },
    { id: 9, dimension: 2, topic: 'Educación', text: '¿Debe priorizarse el presupuesto público de educación superior a las universidades estatales?' },
    { id: 10, dimension: 2, topic: 'Subsidios', text: '¿Es partidario de una Renta Básica Universal sin condiciones para población vulnerable?' },
    { id: 11, dimension: 2, topic: 'Género', text: '¿Es adecuado crear un marco institucional autónomo dedicado a políticas de enfoque de género?' },
    { id: 12, dimension: 2, topic: 'Laboral', text: '¿Debe encarecerse por ley la jornada nocturna para favorecer al trabajador sobre la empresa?' },
    { id: 13, dimension: 3, topic: 'Paz', text: '¿Apoya la negociación política activa con grupos armados (Paz Total)?' },
    { id: 14, dimension: 3, topic: 'Cárceles', text: '¿Debe el país construir mega-cárceles de aislamiento estricto para mitigar la delincuencia?' },
    { id: 15, dimension: 3, topic: 'Glifosato', text: '¿Se debe reactivar la aspersión aérea forzosa de cultivos ilícitos con glifosato?' },
    { id: 16, dimension: 3, topic: 'Policía', text: '¿Debería trasladarse la Policía Nacional desde el Ministerio de Defensa a otro Ministerio?' },
    { id: 17, dimension: 3, topic: 'JEP', text: '¿Debe preservarse la Jurisdicción Especial para la Paz (JEP) sin modificaciones estructurales?' },
    { id: 18, dimension: 3, topic: 'Armas', text: '¿Es conveniente flexibilizar permisos para el porte legítimo de armas para defensa personal?' },
    { id: 19, dimension: 4, topic: 'Autos', text: '¿Se debe prohibir la venta de vehículos de combustión fósil nuevos antes de 2035?' },
    { id: 20, dimension: 4, topic: 'Minería', text: '¿Debe suspenderse la concesión de nuevos contratos de exploración minera a gran escala?' },
    { id: 21, dimension: 4, topic: 'Voto', text: '¿Debería instaurarse el voto obligatorio para contrarrestar la abstención electoral?' },
    { id: 22, dimension: 4, topic: 'Cannabis', text: '¿Es viable legalizar integralmente el uso recreativo y la comercialización del cannabis?' },
    { id: 23, dimension: 4, topic: 'Eutanasia', text: '¿Debe el congreso regular legalmente el acceso al derecho a la muerte digna asistida?' },
    { id: 24, dimension: 4, topic: 'Congreso', text: '¿Se debe reformar la constitución para reducir a la mitad el número total de congresistas?' }
];

// ==========================================
// 2. STATE MANAGEMENT & PERSISTENCE
// ==========================================
window.appState = {
    currentScreen: 0,
    currentQuestionIdx: 0,
    userAnswers: {},
    userWeights: {},
    autosaveTimer: null,
    chatHistory: [] // Nuevo estado para el chat
};

window.addEventListener('DOMContentLoaded', () => {
    loadStateFromStorage();
    renderScreen();
});

function loadStateFromStorage() {
    try {
        const rawSession = localStorage.getItem('voto_informado_session');
        if (rawSession) {
            const parsed = JSON.parse(rawSession);
            window.appState.userAnswers = parsed.userAnswers || {};
            window.appState.userWeights = parsed.userWeights || {};
            window.appState.currentScreen = parsed.currentScreen || 0;
            window.appState.currentQuestionIdx = parsed.currentQuestionIdx || 0;
            window.appState.chatHistory = parsed.chatHistory || [];
        }
    } catch (e) {
        console.error("Error persistencia local:", e);
    }
}

function triggerDebouncedAutosave() {
    if (window.appState.autosaveTimer) clearTimeout(window.appState.autosaveTimer);
    window.appState.autosaveTimer = setTimeout(() => {
        localStorage.setItem('voto_informado_session', JSON.stringify(window.appState));
    }, 300);
}

function clearSessionData() {
    window.appState.userAnswers = {};
    window.appState.userWeights = {};
    window.appState.currentScreen = 0;
    window.appState.currentQuestionIdx = 0;
    window.appState.chatHistory = [];
    localStorage.removeItem('voto_informado_session');
    renderScreen();
}

function navigateTo(screenIndex) {
    window.appState.currentScreen = screenIndex;
    triggerDebouncedAutosave();
    renderScreen();
}

// ==========================================
// 3. UI RENDERING ENGINE
// ==========================================
function renderScreen() {
    const viewport = document.getElementById('app-viewport');
    switch(window.appState.currentScreen) {
        case 0: viewport.innerHTML = buildLandingHTML(); break;
        case 1: viewport.innerHTML = buildQuizLayoutHTML(); updateQuestionCardDOM(); break;
        case 2: viewport.innerHTML = buildReviewHTML(); break;
        case 3: 
            viewport.innerHTML = buildDashboardHTML(); 
            renderDashboardChartsAndVisuals(); 
            initializeChatbot(); // Inicializa el chat al cargar el dashboard
            break;
    }
    window.scrollTo(0,0);
}

function toggleTheme() {
    document.body.classList.toggle('light');
    const btn = document.getElementById('theme-toggle-btn');
    btn.textContent = document.body.classList.contains('light') ? '🌙' : '☀️';
    if (window.appState.currentScreen === 3) renderDashboardChartsAndVisuals();
}

// ==========================================
// 4. CHATBOT ENGINE (API CLIENT)
// ==========================================
function initializeChatbot() {
    const container = document.getElementById('chat-messages');
    if (!container) return;
    container.innerHTML = ''; // Limpiar
    
    // Si no hay historial, agregar mensaje de bienvenida
    if (window.appState.chatHistory.length === 0) {
        const ranking = calculateAfinityMetrics();
        const top = ranking[0];
        window.appState.chatHistory.push({
            role: 'bot',
            text: `¡Hola! Soy Gemini. Analicé tus resultados y noto que tienes una alta afinidad (${top.overallMatch}%) con ${top.name}. ¿Tienes alguna pregunta sobre tus resultados o alguna propuesta específica?`
        });
        triggerDebouncedAutosave();
    }
    
    // Renderizar historial
    window.appState.chatHistory.forEach(msg => appendMessageToDOM(msg.role, msg.text, false));
}

function appendMessageToDOM(role, text, saveToHistory = true) {
    const container = document.getElementById('chat-messages');
    if (!container) return null;
    
    const msgId = 'msg-' + Date.now();
    const msgDiv = document.createElement('div');
    msgDiv.className = `chat-msg ${role}`;
    msgDiv.id = msgId;
    
    // Función de limpieza básica para convertir saltos de línea a <br>
    msgDiv.innerHTML = text.replace(/\n/g, '<br>');
    container.appendChild(msgDiv);
    
    // Auto-scroll
    container.scrollTop = container.scrollHeight;
    
    if (saveToHistory) {
        window.appState.chatHistory.push({ role, text });
        triggerDebouncedAutosave();
    }
    return msgId;
}

function updateMessageInDOM(id, text) {
    const msgDiv = document.getElementById(id);
    if (msgDiv) {
        msgDiv.innerHTML = text.replace(/\n/g, '<br>');
        msgDiv.classList.remove('loading');
        // Actualizar último registro en el historial
        if(window.appState.chatHistory.length > 0) {
            window.appState.chatHistory[window.appState.chatHistory.length - 1].text = text;
            triggerDebouncedAutosave();
        }
        const container = document.getElementById('chat-messages');
        container.scrollTop = container.scrollHeight;
    }
}

window.handleChatKeyPress = function(e) {
    if (e.key === 'Enter') window.sendChatMessage();
};

window.sendChatMessage = async function() {
    const input = document.getElementById('chat-input');
    const text = input.value.trim();
    if (!text) return;
    
    // Deshabilitar input temporalmente
    input.value = '';
    input.disabled = true;
    
    // Renderizar usuario
    appendMessageToDOM('user', text);
    
    // Renderizar loader
    const loadingId = appendMessageToDOM('bot', '<span class="loading-dots">Analizando...</span>');
    document.getElementById(loadingId).classList.add('loading');
    
    const ranking = calculateAfinityMetrics();
    const payload = {
        message: text,
        context: {
            resultado: "Evaluación completada",
            candidato_top: ranking[0]?.name || "Ninguno",
            afinidad: ranking[0]?.overallMatch || 0,
            ranking: ranking.map(r => ({ name: r.name, overallMatch: r.overallMatch })),
            respuestas_usuario: window.appState.userAnswers
        }
    };

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await response.json();
        updateMessageInDOM(loadingId, data.response);
    } catch (error) {
        console.error("Error al comunicarse con Gemini:", error);
        updateMessageInDOM(loadingId, "⚠️ Hubo un error de conexión al consultar a Gemini. Intenta de nuevo.");
    } finally {
        input.disabled = false;
        input.focus();
    }
};

// ==========================================
// 5. VIEW BUILDERS (HTML GENERATORS)
// ==========================================
function buildLandingHTML() {
    let recoveryBanner = '';
    if (Object.keys(window.appState.userAnswers).length > 0) {
        recoveryBanner = `
            <div class="session-banner">
                <div><p style="font-weight: 700;">Tienes un progreso guardado en memoria</p></div>
                <div style="display: flex; gap: 0.75rem;">
                    <button class="btn btn-secondary" onclick="clearSessionData()">Borrar e iniciar de cero</button>
                    <button class="btn btn-primary" onclick="navigateTo(${window.appState.currentScreen || 1})">Continuar progreso</button>
                </div>
            </div>`;
    }
    return `
        ${recoveryBanner}
        <section class="landing-hero">
            <h2 class="landing-title">¿Quién merece tu voto en la Colombia de 2026?</h2>
            <p class="landing-subtitle">Analiza los planes de gobierno reales de los candidatos sin sesgos mediáticos.</p>
            <div class="landing-actions">
                <button class="btn btn-primary" onclick="startFreshQuiz()">Iniciar Diagnóstico</button>
            </div>
        </section>
    `;
}

function startFreshQuiz() {
    window.appState.userAnswers = {};
    window.appState.userWeights = {};
    window.appState.currentQuestionIdx = 0;
    window.appState.chatHistory = [];
    BANK_QUESTIONS.forEach(q => { window.appState.userWeights[q.id] = 2; });
    navigateTo(1);
}

function buildQuizLayoutHTML() {
    return `
        <div class="quiz-layout">
            <aside class="quiz-sidebar">
                <h3 class="sidebar-title">Ejes Electorales</h3>
                <nav class="nav-list" id="sidebar-nav-list">
                    </nav>
            </aside>
            <section class="quiz-main" id="quiz-question-injection-zone"></section>
        </div>
    `;
}

window.registerUserVote = function(voteValue) {
    const q = BANK_QUESTIONS[window.appState.currentQuestionIdx];
    window.appState.userAnswers[q.id] = voteValue;
    triggerDebouncedAutosave();
    setTimeout(() => {
        if (window.appState.currentQuestionIdx < BANK_QUESTIONS.length - 1) {
            window.appState.currentQuestionIdx++;
            updateQuestionCardDOM();
        } else {
            navigateTo(2);
        }
    }, 200);
};

window.setQuestionWeight = function(weight) {
    const q = BANK_QUESTIONS[window.appState.currentQuestionIdx];
    window.appState.userWeights[q.id] = weight;
    updateQuestionCardDOM();
};

function updateQuestionCardDOM() {
    const target = document.getElementById('quiz-question-injection-zone');
    const sidebar = document.getElementById('sidebar-nav-list');
    if (!target) return;

    if(sidebar) {
        sidebar.innerHTML = BANK_QUESTIONS.map((q, idx) => `
            <button class="nav-item ${idx === window.appState.currentQuestionIdx ? 'active' : ''} ${window.appState.userAnswers[q.id] !== undefined ? 'answered' : ''}" onclick="window.appState.currentQuestionIdx=${idx}; updateQuestionCardDOM();">
                <div class="nav-status"></div><span>${q.id}. ${q.topic}</span>
            </button>
        `).join('');
    }

    const q = BANK_QUESTIONS[window.appState.currentQuestionIdx];
    const total = BANK_QUESTIONS.length;
    const answered = Object.keys(window.appState.userAnswers).length;
    const pct = Math.round((answered / total) * 100);
    const uVote = window.appState.userAnswers[q.id];
    const uWeight = window.appState.userWeights[q.id] || 2;

    target.innerHTML = `
        <div class="progress-header">
            <span style="font-size: 0.85rem; font-weight: 600;">Progreso General</span>
            <div class="progress-bar-container"><div class="progress-bar-fill" style="width: ${pct}%;"></div></div>
            <span class="monospace">${answered}/${total}</span>
        </div>
        <div class="question-card">
            <h3 style="font-size: 1.5rem; margin-bottom: 1rem;">${q.text}</h3>
            
            <div style="margin-bottom: 2rem;">
                <p style="font-size: 0.85rem; font-weight: 600; margin-bottom: 0.5rem;">Importancia del eje:</p>
                <div class="weight-buttons">
                    <button class="weight-btn ${uWeight===1?'active':''}" onclick="setQuestionWeight(1)">Baja</button>
                    <button class="weight-btn ${uWeight===2?'active':''}" onclick="setQuestionWeight(2)">Media</button>
                    <button class="weight-btn ${uWeight===3?'active':''}" onclick="setQuestionWeight(3)">Alta</button>
                </div>
            </div>

            <div class="vote-actions">
                <button class="btn btn-vote btn-vote-no ${uVote===0?'active':''}" onclick="registerUserVote(0)">NO</button>
                <button class="btn btn-vote btn-vote-si ${uVote===1?'active':''}" onclick="registerUserVote(1)">SÍ</button>
            </div>
            
            <div class="quiz-navigation">
                <button class="btn btn-secondary" onclick="window.appState.currentQuestionIdx--; updateQuestionCardDOM();" ${window.appState.currentQuestionIdx===0?'disabled':''}>Anterior</button>
                <button class="btn btn-secondary" onclick="navigateTo(2)">Revisar al final</button>
                <button class="btn btn-secondary" onclick="window.appState.currentQuestionIdx++; updateQuestionCardDOM();" ${window.appState.currentQuestionIdx===total-1?'disabled':''}>Siguiente</button>
            </div>
        </div>
    `;
}

function buildReviewHTML() {
    let tableRows = BANK_QUESTIONS.map(q => {
        const ans = window.appState.userAnswers[q.id];
        const w = window.appState.userWeights[q.id] || 2;
        const badge = ans === 1 ? '<span style="color:var(--success);font-weight:bold;">SÍ</span>' : (ans === 0 ? '<span style="color:var(--danger);font-weight:bold;">NO</span>' : 'Falta');
        return `<tr><td>${q.id}</td><td>${q.topic}</td><td>${badge}</td><td>x${w}</td>
                <td><button class="btn btn-secondary" style="padding:0.2rem 0.5rem" onclick="window.appState.currentQuestionIdx=${q.id-1}; navigateTo(1);">Editar</button></td></tr>`;
    }).join('');

    return `
        <div style="max-width: 900px; margin: 0 auto;">
            <h2>Revisión Final</h2>
            <div class="table-responsive">
                <table class="review-table">
                    <thead><tr><th>ID</th><th>Eje Temático</th><th>Respuesta</th><th>Peso</th><th>Acción</th></tr></thead>
                    <tbody>${tableRows}</tbody>
                </table>
            </div>
            <div style="display:flex; justify-content: space-between;">
                <button class="btn btn-secondary" onclick="navigateTo(1)">Volver</button>
                <button class="btn btn-primary" onclick="navigateTo(3)">Ver Resultados</button>
            </div>
        </div>
    `;
}

function calculateAfinityMetrics() {
    let results = {};
    for (const key in CANDIDATES) {
        results[key] = { id: key, score: 0, weightSum: 0, dims: {1:0,2:0,3:0,4:0}, dimW: {1:0,2:0,3:0,4:0} };
    }

    BANK_QUESTIONS.forEach(q => {
        const uAns = window.appState.userAnswers[q.id];
        const w = window.appState.userWeights[q.id] || 2;
        for (const k in CANDIDATES) {
            const cAns = CANDIDATES[k].answers[q.id];
            const match = (uAns !== undefined && uAns === cAns) ? 1 : 0;
            results[k].score += match * w;
            results[k].weightSum += w;
            results[k].dims[q.dimension] += match * w;
            results[k].dimW[q.dimension] += w;
        }
    });

    return Object.values(results).map(r => ({
        ...CANDIDATES[r.id],
        overallMatch: r.weightSum > 0 ? Math.round((r.score / r.weightSum) * 100) : 0,
        dimensions: [1,2,3,4].reduce((acc, d) => ({...acc, [d]: r.dimW[d] > 0 ? (r.dims[d] / r.dimW[d]) * 100 : 0}), {})
    })).sort((a,b) => b.overallMatch - a.overallMatch);
}

function buildDashboardHTML() {
    const ranking = calculateAfinityMetrics();
    const top = ranking[0];
    
    // Mantenemos los gráficos y visuales dentro del área imprimible, y sacamos el Chat fuera de ella
    return `
        <div class="dashboard-grid">
            
            <div id="printable-area">
                <section class="result-hero">
                    <div>
                        <div class="result-affinity-score monospace">${top.overallMatch}%</div>
                        <h2>${top.name}</h2>
                        <p>${top.ideology}</p>
                    </div>
                    <div class="big-avatar" style="--cand-color:${top.color}">${top.avatarText}</div>
                </section>
                
                <div class="viz-row">
                    <div class="viz-card">
                        <h3>Afinidad Comparativa</h3>
                        <div class="radar-container"><canvas id="radarChart"></canvas></div>
                    </div>
                    <div class="viz-card" style="text-align:center;">
                        <h3>Espectro Político</h3>
                        <div class="scatter-container"><div class="scatter-plot-box" id="scatter-box">
                            <div class="scatter-axis-x"></div><div class="scatter-axis-y"></div>
                        </div></div>
                    </div>
                </div>
            </div>

            <section class="chatbot-section">
                <h3>🗣️ Asistente Electoral (Gemini AI)</h3>
                <p style="font-size: 0.85rem; color: var(--muted); margin-bottom: 1rem;">Hazle preguntas específicas sobre tus resultados o pide que te resuma las propuestas de tus candidatos compatibles.</p>
                
                <div class="chat-container">
                    <div class="chat-messages" id="chat-messages">
                        </div>
                    <div class="chat-input-area">
                        <input type="text" id="chat-input" class="chat-input" placeholder="Escribe tu pregunta aquí..." onkeypress="window.handleChatKeyPress(event)">
                        <button class="btn btn-primary chat-send-btn" onclick="window.sendChatMessage()">Enviar</button>
                    </div>
                </div>
            </section>

            <section class="final-actions-row" style="display:flex; justify-content: space-between; gap: 1rem; margin-top: 2rem; padding-top: 2rem; border-top: 1px solid var(--border);">
                <button class="btn btn-secondary" onclick="html2pdf().from(document.getElementById('printable-area')).save()">📥 Exportar PDF</button>
                <button class="btn btn-primary" onclick="clearSessionData()">🔄 Reiniciar Test</button>
            </section>
        </div>
    `;
}

function renderDashboardChartsAndVisuals() {
    const ranking = calculateAfinityMetrics();
    
    // 1. Renderizar Radar
    const ctx = document.getElementById('radarChart');
    if (ctx) {
        new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['Economía', 'Social', 'Seguridad', 'Futuro'],
                datasets: ranking.map(c => ({
                    label: c.name,
                    data: [c.dimensions[1], c.dimensions[2], c.dimensions[3], c.dimensions[4]],
                    borderColor: c.color, backgroundColor: `${c.color}20`
                }))
            },
            options: { responsive: true, maintainAspectRatio: false, scales: { r: { min: 0, max: 100 } } }
        });
    }

    // 2. Renderizar Scatter
    const scatter = document.getElementById('scatter-box');
    if(scatter) {
        scatter.innerHTML = '<div class="scatter-axis-x"></div><div class="scatter-axis-y"></div>'; // reset
        ranking.forEach(c => {
            const left = ((c.x_axis + 1) / 2) * 100;
            const bot = ((c.y_axis + 1) / 2) * 100;
            scatter.innerHTML += `<div class="scatter-dot" style="left:${left}%; bottom:${bot}%; background:${c.color};" title="${c.name}"></div>`;
        });
    }
}
