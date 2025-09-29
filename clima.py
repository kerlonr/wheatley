#!/usr/bin/env python3
# clima.py
import sys
print("Python em uso:", sys.executable)

from flask import Flask, render_template_string, request, jsonify
import requests
import json

app = Flask(__name__)

CULTURAS = {
    "soja": {
        "nome": "Soja",
        "temp": (20, 30),
        "umid_ar": (60, 70),
        "umid_solo": (60, 70),
        "luz": (70, 90),
        "ph": (6.0, 6.8),
        "epoca": "Out-Dez",
        "precipitacao": "500-700mm",
        "profundidade": "3-5cm",
        "adubacao": "NPK 02-20-20",
        "regiao": "Noroeste RS",
        "ciclo": (90, 120)
    },
    "milho": {
        "nome": "Milho",
        "temp": (18, 27),
        "umid_ar": (50, 65),
        "umid_solo": (65, 75),
        "luz": (60, 80),
        "ph": (5.5, 7.0),
        "epoca": "Set-Nov",
        "precipitacao": "600-900mm",
        "profundidade": "4-6cm",
        "adubacao": "NPK 08-28-16",
        "regiao": "Noroeste RS",
        "ciclo": (120, 150)
    },
    "trigo": {
        "nome": "Trigo",
        "temp": (15, 25),
        "umid_ar": (55, 70),
        "umid_solo": (55, 70),
        "luz": (50, 70),
        "ph": (5.5, 7.0),
        "epoca": "Jun-Jul",
        "precipitacao": "400-600mm",
        "profundidade": "2-4cm",
        "adubacao": "NPK 10-20-10",
        "regiao": "Noroeste RS",
        "ciclo": (90, 110)
    },
    "aveia": {
        "nome": "Aveia",
        "temp": (12, 22),
        "umid_ar": (50, 65),
        "umid_solo": (50, 65),
        "luz": (40, 60),
        "ph": (5.0, 6.5),
        "epoca": "Abr-Mai",
        "precipitacao": "300-500mm",
        "profundidade": "2-3cm",
        "adubacao": "NPK 05-20-15",
        "regiao": "Noroeste RS",
        "ciclo": (120, 150)
    }
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wheathley - ESP LoRa32</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link rel="icon" type="image/webp" href="https://icones.pro/wp-content/uploads/2021/07/icone-meteo-verte.png">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.4.0/dist/leaflet.css" />

    <style>
:root {
    --dark-bg: #121212;
    --card-bg: #1e1e1e;
    --text-primary: #f0f0f0;
    --text-secondary: #a0a0a0;
    --accent-color: #4a6cf7;
    --excellent-signal: #4CAF50;
    --good-signal: #8BC34A;
    --medium-signal: #FFC107;
    --poor-signal: #FF9800;
    --bad-signal: #F44336;
    --good-status: #4CAF50;
    --warning-status: #FFC107;
    --bad-status: #F44336;
}

body {
    background-color: var(--dark-bg);
    color: var(--text-primary);
    padding: 20px;
    font-family: 'Inter', sans-serif;
}

.container {
    max-width: 1000px;
    margin: 0 auto;
}

h1 {
    text-align: center;
    margin-bottom: 30px;
    font-weight: 500;
}

.top-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
    margin-bottom: 15px;
}

.sensor-card {
    background-color: var(--card-bg);
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    text-align: center;
    border: 1px solid #2a2a2a;
}

.signal-card {
    grid-column: span 4;
    background-color: var(--card-bg);
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    border: 1px solid #2a2a2a;
}

.card-header {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    margin-bottom: 15px;
}

.card-icon {
    font-size: 24px;
    color: var(--accent-color);
}

.card-value {
    text-align: center;
    font-size: 2rem;
    font-weight: 300;
    margin: 10px 0;
}

.card-unit {
    font-size: 1rem;
    color: var(--text-secondary);
}

.signal-bar {
    height: 10px;
    background: linear-gradient(90deg,
        var(--bad-signal) 0%,
        var(--poor-signal) 25%,
        var(--medium-signal) 50%,
        var(--good-signal) 75%,
        var(--excellent-signal) 100%);
    border-radius: 5px;
    margin: 20px 0 10px;
    position: relative;
}

.signal-pointer {
    position: absolute;
    top: -6px;
    left: 0%;
    transform: translateX(-50%);
    width: 0;
    height: 0;
    border-left: 6px solid transparent;
    border-right: 6px solid transparent;
    border-top: 10px solid white;
}

.battery-level {
    position: relative;
    width: 120px;
    height: 24px;
    margin: 12px auto;
    background: #2a2a2a;
    border-radius: 4px;
    overflow: hidden;
    border: 1px solid #3a3a3a;
}

.battery-fill {
    height: 100%;
    background: var(--accent-color);
    transition: width 0.5s ease;
    box-shadow: inset 0 1px 2px rgba(255,255,255,0.1);
}

.battery-percent {
    position: absolute;
    right: 8px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 0.75rem;
    color: var(--text-primary);
    mix-blend-mode: difference;
}

.plantio-section {
    background: var(--card-bg);
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    border: 1px solid #2a2a2a;
}

.plantio-section h2 {
    font-size: 1.25rem;
    margin-bottom: 1.2rem;
    color: var(--accent-color);
    text-align: center;
    font-weight: 500;
}

.condicoes-list {
    display: grid;
    gap: 0.8rem;
    margin: 1.5rem 0;
}

.condicao-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.8rem 1rem;
    background: #2a2a2a;
    border-radius: 8px;
    border: 1px solid #3a3a3a;
    transition: transform 0.2s ease;
}

.condicao-item:hover {
    transform: translateX(4px);
}

.status-indicator {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    margin-left: 0.8rem;
    box-shadow: 0 0 8px currentColor;
}

.good { color: var(--excellent-signal); }
.warning { color: var(--medium-signal); }
.bad { color: var(--bad-signal); }

select {
    background: #2a2a2a;
    border: 1px solid #3a3a3a;
    color: var(--text-primary);
    padding: 0.8rem 1.2rem;
    border-radius: 8px;
    width: 100%;
    margin-bottom: 1.5rem;
    appearance: none;
}

.detail-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 1rem;
    margin-top: 1.5rem;
}

.detail-card {
    background: #2a2a2a;
    padding: 1.2rem;
    border-radius: 8px;
    border: 1px solid #3a3a3a;
}

.detail-label {
    font-size: 0.75rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.5rem;
}

.detail-value {
    font-size: 1rem;
    color: var(--text-primary);
    font-weight: 500;
}

.signal-labels {
    display: flex;
    justify-content: space-between;
    margin-top: 5px;
    font-size: 0.7rem;
    color: var(--text-secondary);
}

.signal-info {
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
}

.signal-quality {
    font-weight: 500;
}

/* Windy iframe styles */
.windy-section {
    grid-column: span 4;
    background: var(--card-bg);
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    border: 1px solid #2a2a2a;
}

.windy-iframe-wrapper {
    width: 100%;
    height: 0;
    padding-bottom: 60%;
    position: relative;
    overflow: hidden;
    border-radius: 8px;
    margin-top: 15px;
}

.windy-iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    color: var(--text-secondary);
    background: var(--card-bg);
}

.windy-loading i {
    font-size: 2rem;
    margin-bottom: 10px;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

@media (max-width: 600px) {
    .windy-section { grid-column: auto; }
    .top-row { grid-template-columns: 1fr; }
    .sensor-card, .signal-card { grid-column: span 1; }
    .detail-grid { grid-template-columns: 1fr; }
    .condicao-item { font-size: 0.9rem; padding: 0.6rem; }
    .card-value { font-size: 1.8rem; }
}

@media (max-width: 768px) {
    .windy-iframe-wrapper { padding-bottom: 80%; }
}

@media (max-width: 480px) {
    .windy-iframe-wrapper { padding-bottom: 100%; }
}
    </style>
</head>

<body>
    <div class="container">
        <h1>Monitor Ambiental</h1>

        <div class="top-row">
            <!-- Bateria -->
            <div class="sensor-card">
                <div class="card-header">
                    <i class="fas fa-battery-full card-icon"></i>
                    <div>Bateria</div>
                </div>
                <div class="battery-level">
                    <div class="battery-fill" style="width: 0%;"></div>
                    <div class="battery-percent">0%</div>
                </div>
            </div>

            <!-- Temperatura -->
            <div class="sensor-card">
                <div class="card-header">
                    <i class="fas fa-thermometer-half card-icon"></i>
                    <div>Temperatura</div>
                </div>
                <div class="card-value" id="temperatura">--<span class="card-unit">°C</span></div>
            </div>

            <!-- Umidade -->
            <div class="sensor-card">
                <div class="card-header">
                    <i class="fas fa-tint card-icon"></i>
                    <div>Umidade</div>
                </div>
                <div class="card-value" id="umidade">--<span class="card-unit">%</span></div>
            </div>

            <!-- Luminosidade -->
            <div class="sensor-card">
                <div class="card-header">
                    <i class="fas fa-sun card-icon"></i>
                    <div>Luminosidade</div>
                </div>
                <div class="card-value" id="luminosidade">--<span class="card-unit">%</span></div>
            </div>

            <div class="signal-card">
                <div class="card-header">
                    <i class="fas fa-wifi card-icon"></i>
                    <div>Qualidade do Sinal</div>
                </div>
                <div class="card-value" id="rssi">--<span class="card-unit">dBm</span></div>

                <div class="signal-bar">
                    <div class="signal-pointer" id="signal-pointer"></div>
                </div>

                <div class="signal-labels">
                    <span>Muito Ruim</span>
                    <span>Ruim</span>
                    <span>Regular</span>
                    <span>Bom</span>
                    <span>Excelente</span>
                </div>

                <div class="signal-info">
                    <span id="snr">SNR: -- dB</span>
                    <span class="signal-quality" id="signal-quality">--</span>
                </div>
            </div>

            <!-- Windy -->
            <div class="windy-section">
                <h2 style="display:flex;justify-content:center;margin:0; gap:10px; font-weight:100;">
                    <i class="fas fa-wind card-icon"></i>Mapa Climático
                </h2>
                <div class="windy-iframe-wrapper">
                    <div class="windy-loading" id="windy-loading">
                        <i class="fas fa-spinner"></i>
                        <span>Carregando mapa meteorológico...</span>
                    </div>
                    <iframe class="windy-iframe" id="windy-iframe" src="about:blank" allow="geolocation"
                            onload="document.getElementById('windy-loading').style.display = 'none';"></iframe>
                </div>
            </div>
        </div>

        <!-- Seção plantio / seleção de cultura -->
        <div class="plantio-section">
            <h2>Condições de Plantio</h2>
            <select id="cultura"></select>
            <div id="condicoes" class="condicoes-list"></div>
        </div>
    </div>

    <script src="https://unpkg.com/leaflet@1.4.0/dist/leaflet.js"></script>

<script>
const CULTURAS = {{culturas_json|safe}};

function getStatusClass(valor, min, max) {
    if (valor >= min && valor <= max) return 'good';
    if (Math.abs(valor - min) <= 2 || Math.abs(valor - max) <= 2) return 'warning';
    return 'bad';
}

function atualizarCondicoesComDados(data) {
    const culturaKey = document.getElementById('cultura').value;
    const condicoes = CULTURAS[culturaKey];
    if (!condicoes) return;

    const valores = {
        temperatura: data.temperatura,
        umidade: data.umidade,
        luminosidade: data.luminosidade,
        ph: data.ph ?? 6.5,
        umid_solo: data.umid_solo ?? 60
    };

    const htmlParts = [];

    // Temperatura
    htmlParts.push(`
        <div class="condicao-item">
            <span>Temperatura (${condicoes.temp[0]}°C - ${condicoes.temp[1]}°C)</span>
            <div class="status-indicator ${getStatusClass(valores.temperatura, condicoes.temp[0], condicoes.temp[1])}"></div>
        </div>
    `);

    // Umidade do ar
    htmlParts.push(`
        <div class="condicao-item">
            <span>Umidade do ar (${condicoes.umid_ar[0]}% - ${condicoes.umid_ar[1]}%)</span>
            <div class="status-indicator ${getStatusClass(valores.umidade, condicoes.umid_ar[0], condicoes.umid_ar[1])}"></div>
        </div>
    `);

    // Luminosidade
    htmlParts.push(`
        <div class="condicao-item">
            <span>Luminosidade (${condicoes.luz[0]}% - ${condicoes.luz[1]}%)</span>
            <div class="status-indicator ${getStatusClass(valores.luminosidade, condicoes.luz[0], condicoes.luz[1])}"></div>
        </div>
    `);

    // pH (se disponível)
    if (condicoes.ph) {
        htmlParts.push(`
            <div class="condicao-item">
                <span>pH (${condicoes.ph[0]} - ${condicoes.ph[1]})</span>
                <div class="status-indicator ${getStatusClass(valores.ph, condicoes.ph[0], condicoes.ph[1])}"></div>
            </div>
        `);
    }

    // Umidade do solo
    htmlParts.push(`
        <div class="condicao-item">
            <span>Umidade do solo (${condicoes.umid_solo[0]}% - ${condicoes.umid_solo[1]}%)</span>
            <div class="status-indicator ${getStatusClass(valores.umid_solo, condicoes.umid_solo[0], condicoes.umid_solo[1])}"></div>
        </div>
    `);

    document.getElementById('condicoes').innerHTML = htmlParts.join('');
}

function aplicarDadosNaUI(data) {
    // Bateria
    const bateriaFill = document.querySelector('.battery-fill');
    const bateriaPercent = document.querySelector('.battery-percent');
    const bateriaVal = data.bateria ?? 0;
    bateriaFill.style.width = `${bateriaVal}%`;
    bateriaPercent.textContent = `${bateriaVal}%`;
    bateriaFill.style.background = data.battery_color || '';

    // Sensores
    document.getElementById('temperatura').innerHTML = `${data.temperatura ?? '--'}<span class="card-unit">°C</span>`;
    document.getElementById('umidade').innerHTML = `${data.umidade ?? '--'}<span class="card-unit">%</span>`;
    document.getElementById('luminosidade').innerHTML = `${data.luminosidade ?? '--'}<span class="card-unit">%</span>`;

    // Sinal
    document.getElementById('rssi').innerHTML = `${data.rssi ?? '--'}<span class="card-unit">dBm</span>`;
    document.getElementById('snr').textContent = `SNR: ${data.snr ?? '--'} dB`;
    document.getElementById('signal-quality').textContent = data.signal_quality ?? '--';

    // Ponteiro do sinal
    const pointer = document.getElementById('signal-pointer');
    const perc = data.signal_percentage ?? 0;
    const bounded = Math.max(0, Math.min(100, perc));
    // coloca dentro da barra (ajuste left)
    pointer.style.left = bounded + '%';

    // Atualiza as condições de plantio com os dados atuais
    atualizarCondicoesComDados(data);
}

let ultimoDados = null;
function atualizarDados() {
    fetch('/dados_sensores')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Erro no endpoint:', data.error);
                return;
            }
            ultimoDados = data;
            aplicarDadosNaUI(data);
        })
        .catch(error => console.error('Erro:', error));
}

function popularCulturaSelect() {
    const sel = document.getElementById('cultura');
    sel.innerHTML = '';
    for (const key in CULTURAS) {
        const opt = document.createElement('option');
        opt.value = key;
        opt.textContent = CULTURAS[key].nome || key;
        sel.appendChild(opt);
    }
    sel.addEventListener('change', () => {
        if (ultimoDados) atualizarCondicoesComDados(ultimoDados);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    popularCulturaSelect();
    atualizarDados();
    setInterval(atualizarDados, 5000); // atualiza a cada 5s
});
</script>

<script>
    // Função para carregar o mapa Windy
    function loadWindyMap() {
        const iframe = document.getElementById('windy-iframe');
        const loadingDiv = document.getElementById('windy-loading');
        const lat = -28.26;
        const lon = -54.17;
        const zoom = 8;

        const windyUrl = `https://embed.windy.com/embed2.html?lat=${lat}&lon=${lon}&zoom=${zoom}&level=surface&overlay=wind&menu=&message=true&marker=true&calendar=now&pressure=&type=map&location=coordinates&detail&metricWind=km%2Fh&metricTemp=%C2%B0C`;
        iframe.src = windyUrl;

        iframe.onload = function() {
            loadingDiv.style.display = 'none';
            setTimeout(() => {
                iframe.style.height = '100%';
                iframe.style.width = '100%';
            }, 100);
        };

        setTimeout(() => {
            if (loadingDiv.style.display !== 'none') {
                loadingDiv.innerHTML = `
                    <i class="fas fa-exclamation-triangle"></i>
                    <p>Não foi possível carregar o mapa</p>
                    <a href="${windyUrl}" target="_blank" style="color: var(--accent-color); margin-top: 10px;">
                        Abrir Windy em nova janela
                    </a>
                `;
            }
        }, 15000);
    }

    document.addEventListener('DOMContentLoaded', function() {
        loadWindyMap();
        window.addEventListener('resize', function() {
            const iframe = document.getElementById('windy-iframe');
            if (iframe) {
                iframe.style.height = '100%';
                iframe.style.width = '100%';
            }
        });
    });
</script>

</body>
</html>
"""

def get_battery_color(percent):
    if percent > 70:
        return "#4CAF50"
    elif percent > 30:
        return "#FFC107"
    else:
        return "#F44336"

def get_signal_quality(rssi):
    """Classifica a qualidade do sinal com base no RSSI"""
    try:
        rssi = int(rssi)
    except Exception:
        return ("Desconhecido", "var(--bad-signal)")
    if rssi >= -50: return ("Excelente", "var(--excellent-signal)")
    elif rssi >= -60: return ("Muito Bom", "var(--good-signal)")
    elif rssi >= -70: return ("Bom", "var(--medium-signal)")
    elif rssi >= -80: return ("Regular", "var(--poor-signal)")
    elif rssi >= -90: return ("Ruim", "var(--bad-signal)")
    else: return ("Muito Ruim", "var(--bad-signal)")

def get_signal_percentage(rssi):
    """Converte RSSI para porcentagem (0-100%) para a barra de qualidade.
       Formula simples: -30 dBm -> ~100%, -100 dBm -> ~0%"""
    try:
        r = int(rssi)
    except Exception:
        return 0
    # map -100..-30 to 0..100
    pct = (r + 100) * (100 / 70)
    return max(0, min(100, int(pct)))

@app.route('/')
def index():
    try:
        # tenta obter dados do receptor; pode falhar em dev
        response = requests.get('http://receptor.local/data', timeout=2)
        data = response.json()
    except Exception:
        # valores defaults se receptor indisponível
        data = {
            'bateria': 0,
            'ph': 6.5,
            'umid_solo': 60,
            'hostname': 'desconhecido',
            'temperatura': '--',
            'umidade': '--',
            'luminosidade': '--',
            'rssi': -100,
            'snr': '--',
            'ultimaAtualizacao': '--'
        }

    quality, color = get_signal_quality(data.get('rssi'))
    signal_pct = get_signal_percentage(data.get('rssi'))

    return render_template_string(
        HTML_TEMPLATE,
        bateria=data.get('bateria', 0),
        battery_color=get_battery_color(data.get('bateria', 0)),
        ph=data.get('ph', 6.5),
        umid_solo=data.get('umid_solo', 60),
        hostname=data.get('hostname', 'desconhecido'),
        temperatura=data.get('temperatura', '--'),
        umidade=data.get('umidade', '--'),
        luminosidade=data.get('luminosidade', '--'),
        rssi=data.get('rssi', -100),
        snr=data.get('snr', '--'),
        ultimaAtualizacao=data.get('ultimaAtualizacao', '--'),
        signal_quality=quality,
        signal_color=color,
        signal_percentage=signal_pct,
        culturas_json=json.dumps(CULTURAS)
    )

@app.route('/dados_sensores')
def dados_sensores():
    try:
        response = requests.get('http://receptor.local/data', timeout=2)
        data = response.json()
    except Exception as e:
        # retorna defaults para o frontend não quebrar
        data = {
            'hostname': 'desconhecido',
            'temperatura': None,
            'umidade': None,
            'luminosidade': None,
            'rssi': -100,
            'snr': None,
            'ultimaAtualizacao': None,
            'bateria': 0,
            'ph': 6.5,
            'umid_solo': 60
        }

    quality, color = get_signal_quality(data.get('rssi'))
    return jsonify({
        'hostname': data.get('hostname'),
        'temperatura': data.get('temperatura'),
        'umidade': data.get('umidade'),
        'luminosidade': data.get('luminosidade'),
        'rssi': data.get('rssi'),
        'snr': data.get('snr'),
        'ultimaAtualizacao': data.get('ultimaAtualizacao'),
        'bateria': data.get('bateria', 0),
        'ph': data.get('ph', 6.5),
        'umid_solo': data.get('umid_solo', 60),
        'signal_quality': quality,
        'signal_color': color,
        'signal_percentage': get_signal_percentage(data.get('rssi'))
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
