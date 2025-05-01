# Scientific_Calculator
 
# 🧠📐 Intelligent Expression Interpreter

Uma aplicação interativa com IA para interpretar expressões aritméticas a partir de texto digitado ou imagens. Usa técnicas de OCR, processamento de linguagem natural (NLP) e análise sintática para corrigir e avaliar expressões matemáticas com precisão.

---

## 🚀 Funcionalidades

- 📸 Leitura de expressões matemáticas a partir de imagens usando OCR (Tesseract).
- ✍️ Correção inteligente de entradas ruidosas usando o modelo BERT.
- 🧮 Avaliação manual de expressões com suporte a precedência de operadores.
- 🌐 Visualização da árvore sintática das expressões com NetworkX.
- 🧠 Detecção e sugestão de correções com NLP.

---

## 🛠️ Instalação e Configuração

### 1. Clone o repositório:
git clone https://github.com/GabrielPascoal/Scientific_Calculator.git
cd https://github.com/GabrielPascoal/Scientific_Calculator.git

### 2. Crie e ative o ambiente virtual:
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

### 3. Instale as dependências:
pip install -r requirements.txt

### 4. Instale o Tesseract OCR:
Windows: Baixe e instale via: https://github.com/UB-Mannheim/tesseract/wiki
Linux (Debian/Ubuntu): sudo apt install tesseract-ocr
macOS: brew install tesseract
Após a instalação no Windows, inclua o caminho manualmente no seu script Python, se necessário:
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

### 5. Execute a aplicação:
streamlit run app.py
