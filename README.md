# 🌱 Wheatlhey - Monitor Climático da Horta SETREM

## 📋 Sobre o Projeto

Sistema de monitoramento climático para a horta da SETREM que coleta dados ambientais e os transmite via LoRa para um gateway, que então envia as informações para um banco de dados no LARCC.

## 🎯 Funcionalidades

- **Coleta de Dados Ambientais**:
  - 🌡️ Temperatura do ar
  - 💧 Umidade do ar
  - 🌫️ Pressão atmosférica
  - 🌱 Umidade do solo

- **Tecnologia de Transmissão**:
  - 📡 Comunicação LoRa de longo alcance
  - 🖥️ Gateway receptor de dados
  - 🗄️ Banco de dados no LARCC

## 🛠️ Tecnologias Utilizadas

- **Hardware**: Sensores DHT22, BMP280, Sensor de Umidade do Solo
- **Comunicação**: LoRa (Long Range)
- **Backend**: Gateway com ESP32/Arduino
- **Banco de Dados**: PostgreSQL/MySQL no LARCC
- **Frontend**: HTML, CSS, JavaScript

## 📊 Dados Monitorados

| Sensor | Parâmetro | Unidade |
|--------|-----------|---------|
| DHT22 | Temperatura | °C |
| DHT22 | Umidade do Ar | % |
| BMP280 | Pressão Atmosférica | hPa |
| Sensor Solo | Umidade do Solo | % |

## 🚀 Como Funciona

1. **Coleta**: Sensores capturam dados ambientais
2. **Transmissão**: Dados enviados via LoRa para o gateway
3. **Processamento**: Gateway recebe e processa os dados
4. **Armazenamento**: Dados salvos no banco do LARCC
5. **Visualização**: Interface web exibe informações em tempo real

## 🎨 Interface Web

A interface mostra:
- ✅ Dados em tempo real dos sensores
- 📈 Gráficos de variação temporal
- ⚠️ Alertas de condições críticas
- 📱 Design responsivo para celular

## 🔧 Desenvolvimento

**Equipe SETREM** - Projeto de monitoramento ambiental para agricultura de precisão

---

*Sistema desenvolvido para otimizar o cultivo na horta da SETREM através do monitoramento climático em tempo real.*
