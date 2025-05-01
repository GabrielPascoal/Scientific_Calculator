# 1  - Importação das bibliotecas necessárias

# 2  - Streamlit é uma biblioteca para criar interfaces interativas de maneira rápida e fácil.
import streamlit as st

# 3  - Pytesseract é uma ferramenta de OCR (Reconhecimento Óptico de Caracteres) que converte texto em imagens em texto editável.
import pytesseract

# 4  - OpenCV é uma biblioteca de processamento de imagens que é usada para manipular imagens e vídeos.
import cv2

# 5  - NumPy é uma biblioteca fundamental para o cálculo numérico em Python. Ela oferece suporte a arrays e matrizes multidimensionais.
import numpy as np

# 6  - Matplotlib é uma biblioteca para criar gráficos e visualizações de dados em Python.
import matplotlib.pyplot as plt

# 7  - NetworkX é uma biblioteca para criação, manipulação e estudo da estrutura de redes complexas.
import networkx as nx

# 8  - Pillow é uma biblioteca que permite abrir, manipular e salvar arquivos de imagem.
from PIL import Image

# 9  - BytesIO é usado para manipulação de objetos binários em memória, como arquivos em formato de imagem.
from io import BytesIO

# 10 - Hugging Face Transformers é uma biblioteca para utilizar modelos pré-treinados, como o BERT, para várias tarefas de NLP.
from transformers import pipeline

# 11 - Re é a biblioteca de expressões regulares usada para processar e corrigir expressões.
import re

# 12 - Configuração da página e título da interface do Streamlit
st.set_page_config(page_title="Intelligent Expression Interpreter", layout="wide")  # Define o título e layout da página

# 13 - Exibe o título principal da aplicação na interface do usuário
st.title("🧠📐 Intelligent Expression Interpreter")

# 14 - Exibe uma breve descrição de como usar o sistema
st.write("Digite uma expressão aritmética ou envie uma imagem contendo uma expressão. A IA cuidará do resto!")

# 15 - Função que realiza a correção da expressão digitada
def corrigir_expressao(expressao):
    # 16 - Remove espaços extras e converte tudo para minúsculo
    expressao = expressao.lower().strip()
    # 17 - Substitui símbolos equivalentes por operadores padrão
    expressao = expressao.replace('x', '').replace('×', '').replace('÷', '/').replace('^', '')
    # 18 - Elimina operadores duplicados como "++" ou "/"
    expressao = re.sub(r'(\D)(\1)+', r'\1', expressao)
    # 19 - Remove caracteres inválidos (qualquer coisa que não seja número ou operador)
    expressao = re.sub(r'[^0-9+\-*/(). ]+', '', expressao)
    # 20 - Retorna a expressão já limpa
    return expressao

# 21 - Função para avaliar a expressão usando regras manuais de precedência
def avaliar_expressao_manual(tokens):
    # 22 - Função interna para parsear recursivamente os tokens com base na precedência
    def parse_expression(index):
        # 23 - Inicializa pilhas de operandos e operadores
        valores, operadores = [], []

        # 24 - Aplica o último operador na pilha às variáveis
        def aplicar_op():
            b = valores.pop()  # Operando direito
            a = valores.pop()  # Operando esquerdo
            op = operadores.pop()  # Operador a ser aplicado
            if op == '+': valores.append(a + b)
            elif op == '-': valores.append(a - b)
            elif op == '*': valores.append(a * b)
            elif op == '/': valores.append(a / b)
            elif op == '': valores.append(a ** b)

        # 25 - Define a precedência dos operadores
        def prioridade(op):
            return {'+':1, '-':1, '':2, '/':2, '*':3}.get(op, 0)

        # 26 - Laço principal de análise da expressão
        while index < len(tokens):
            token = tokens[index]
            if token == '(':
                # 27 - Trata subexpressões dentro de parênteses
                res, index = parse_expression(index + 1)
                valores.append(res)
            elif token == ')':
                # 28 - Fim do escopo de parênteses
                break
            elif token in '+-/*':
                # 29 - Processa operadores com base na precedência
                while operadores and prioridade(operadores[-1]) >= prioridade(token):
                    aplicar_op()
                operadores.append(token)
            else:
                # 30 - Adiciona números convertidos para float
                valores.append(float(token))
            index += 1

        # 31 - Aplica operadores restantes após o fim da expressão
        while operadores:
            aplicar_op()
        return valores[0], index  # 32 - Retorna o valor calculado e o índice final

    resultado, _ = parse_expression(0)  # 33 - Inicia o parser a partir do índice 0
    return resultado  # 34 - Retorna o resultado final da expressão

# 35 - Função que converte a string da expressão em uma lista de tokens
def tokenizar(expr):
    # 36 - Expressão regular para capturar números e operadores
    token_pattern = r'\d+\.\d+|\d+|\\|[+\-*/()]'
    return re.findall(token_pattern, expr)  # 37 - Retorna todos os tokens encontrados

# 38 - Função para gerar a árvore sintática da expressão usando grafos
def gerar_arvore(tokens):
    G = nx.DiGraph()  # 39 - Cria um grafo direcionado

    # 40 - Função auxiliar para adicionar nós ao grafo
    def add_nodes(index, parent=None):
        token = tokens[index]  # 41 - Obtém o token atual
        node_id = f"{token}-{index}"  # 42 - Cria um ID único para o nó
        G.add_node(node_id, label=token)  # 43 - Adiciona o nó ao grafo com seu rótulo
        if parent:
            G.add_edge(parent, node_id)  # 44 - Conecta o nó ao pai
        return node_id  # 45 - Retorna o ID do nó

    last_id = None  # 46 - ID do último nó adicionado
    for i, t in enumerate(tokens):  # 47 - Itera sobre os tokens
        last_id = add_nodes(i, last_id if i > 0 else None)  # 48 - Cria os nós encadeados
    return G  # 49 - Retorna o grafo completo

# 50 - Função que exibe a árvore sintática no Streamlit
def exibir_arvore(G):
    pos = nx.spring_layout(G)  # 51 - Define a posição dos nós
    labels = nx.get_node_attributes(G, 'label')  # 52 - Obtém os rótulos dos nós
    plt.figure(figsize=(10, 5))  # 53 - Define o tamanho da imagem
    nx.draw(G, pos, with_labels=True, labels=labels, node_color='skyblue', node_size=1500, font_size=10)  # 54 - Desenha o grafo
    st.pyplot(plt)  # 55 - Exibe o gráfico no app

# 56 - Função que utiliza IA (modelo da Hugging Face) para correção semântica da expressão
def corrigir_com_ia(texto):
    model_name = "bert-base-uncased"  # 57 - Modelo BERT padrão
    nlp = pipeline("fill-mask", model=model_name)  # 58 - Pipeline para preencher lacunas

    # 59 - Verifica se há letras no texto (sinais de ruído textual)
    if any(c.isalpha() for c in texto):
        texto_com_mask = texto.replace(" x ", " [MASK] ").replace(" vezes ", " [MASK] ").replace("por", "[MASK]")  # 60 - Substitui palavras ambíguas por máscara
        try:
            predictions = nlp(texto_com_mask)  # 61 - Tenta prever a palavra correta
            corrected_text = predictions[0]['sequence']  # 62 - Pega a primeira sugestão
            corrected_text = re.sub(r'\[.*?\]', '', corrected_text).strip()  # 63 - Remove tokens especiais
        except Exception as e:
            corrected_text = texto  # 64 - Em caso de erro, retorna o original
        return corrected_text  # 65 - Retorna o texto corrigido
    else:
        return texto  # 66 - Retorna o original se não houver correções necessárias

# 67 - Campo para digitar expressão aritmética
expr_input = st.text_input("Digite a expressão:", placeholder="Ex: (5 + 2) * 3")

# 68 - Permite o envio de imagem com a expressão aritmética
imagem = st.file_uploader("Ou envie uma imagem contendo uma expressão:", type=["png", "jpg", "jpeg"])

# 69 - Inicializa a variável da expressão
expressao = ""

# 70 - Verifica se o usuário enviou uma imagem
if imagem:
    try:
        img = Image.open(imagem)  # 71 - Abre a imagem enviada
        img_np = np.array(img)  # 72 - Converte a imagem para array NumPy
        text = pytesseract.image_to_string(img_np, config='--psm 6')  # 73 - Aplica OCR
        st.write(f"📸 Texto extraído da imagem: {text.strip()}")  # 74 - Exibe o texto extraído
        expressao = text.strip()  # 75 - Armazena o texto para uso posterior
    except Exception as e:
        st.error(f"Erro no OCR: {e}")  # 76 - Mostra erro caso OCR falhe

# 77 - Se não houver imagem mas houver texto digitado
elif expr_input:
    expressao = expr_input  # 78 - Usa a expressão digitada

# 79 - Verifica se há uma expressão a processar
if expressao:
    corrigida = corrigir_expressao(expressao)  # 80 - Aplica correção manual
    st.write(f"✅ Expressão corrigida (pré-processada): {corrigida}")  # 81 - Exibe a expressão corrigida

    expressao_ia = corrigir_com_ia(corrigida)  # 82 - Aplica correção semântica com IA
    st.write(f"✅ Expressão corrigida pela IA: {expressao_ia}")  # 83 - Mostra resultado da IA

    try:
        tokens = tokenizar(expressao_ia)  # 84 - Tokeniza a expressão
        resultado = avaliar_expressao_manual(tokens)  # 85 - Avalia manualmente a expressão
        st.success(f"Resultado: {resultado}")  # 86 - Mostra o resultado

        G = gerar_arvore(tokens)  # 87 - Gera grafo da árvore sintática
        st.write("📊 Árvore Sintática:")  # 88 - Título para a árvore
        exibir_arvore(G)  # 89 - Exibe o grafo

    except Exception as e:
        st.error(f"Erro na avaliação da expressão: {e}")  # 90 - Trata possíveis erros