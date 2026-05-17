import streamlit as st
import requests
import base64
from PIL import Image

# ==========================================
# 🎨 DESIGN COMPACTO E CLEAN (ROXO NEON)
# ==========================================
st.set_page_config(page_title="SinoScan", page_icon="🔍", layout="centered")

# Injeta o visual escuro e moderno direto na tela
st.markdown("""
    <style>
    /* Fundo principal do app */
    .stApp {
        background-color: #0b0f19 !important;
    }
    /* Cor de todos os textos */
    h1, p, label, .stMarkdown {
        color: #f8fafc !important;
    }
    /* Estilização do Botão Analisar */
    div.stButton > button:first-child {
        background-color: #a855f7 !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        width: 100% !important;
        box-shadow: 0px 4px 15px rgba(168, 85, 247, 0.4) !important;
    }
    /* Efeito ao passar o dedo/clicar no botão */
    div.stButton > button:first-child:hover {
        background-color: #9333ea !important;
    }
    /* Caixa de Upload e Inputs mais cleans */
    .stTextInput>div>div>input, .stFileUploader {
        background-color: #1e293b !important;
        color: white !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 📱 CONTEÚDO DO APLICATIVO
# ==========================================

st.title("🔍 Meu Analisador de Anúncios")
st.write("Faça o upload do print do anúncio para analisar os detalhes.")

api_key = st.text_input("Insira sua Gemini API Key:", type="password")
arquivo_image = st.file_uploader("Escolha o print do anúncio:", type=["jpg", "jpeg", "png"])

if arquivo_image:
    imagem = Image.open(arquivo_image)
    st.image(imagem, caption="Imagem carregada", use_container_width=True)

instrucoes = """
Você é um assistente especialista em analisar prints de anúncios de produtos.
Olhe para a imagem e retorne:
1. O nome do produto e a marca.
2. O preço estimado.
3. Se o anúncio parece confiável ou se há pontos de atenção.
"""

if st.button("Analisar Imagem"):
    if not api_key:
        st.error("Insira a sua API Key primeiro!")
    elif not arquivo_image:
        st.error("Suba uma imagem primeiro!")
    else:
        with st.spinner("Analisando diretamente nos servidores do Google..."):
            try:
                chave_limpa = api_key.strip()
                bytes_data = arquivo_image.getvalue()
                base64_image = base64.b64encode(bytes_data).decode('utf-8')
                mime_type = arquivo_image.type

                url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={chave_limpa}"
                headers = {'Content-Type': 'application/json'}
                
                payload = {
                    "contents": [
                        {
                            "parts": [
                                {"text": instrucoes},
                                {
                                    "inlineData": {
                                        "mimeType": mime_type,
                                        "data": base64_image
                                    }
                                }
                            ]
                        }
                    ]
                }
                
                response = requests.post(url, headers=headers, json=payload)
                response_data = response.json()
                
                if response.status_code == 200:
                    try:
                        texto_analise = response_data['candidates'][0]['content']['parts'][0]['text']
                        st.success("Análise Concluída com Sucesso!")
                        st.write(texto_analise)
                    except KeyError:
                        st.error("O Google respondeu, mas os dados vieram bagunçados. Tente enviar a imagem novamente.")
                else:
                    mensagem_erro = response_data.get('error', {}).get('message', 'Erro desconhecido')
                    st.error(f"Erro vindo direto do Google: {mensagem_erro}")
                    
            except Exception as e:
                st.error(f"Erro na conexão direta: {e}")
