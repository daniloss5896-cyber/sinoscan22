import streamlit as st
import requests
import base64
from PIL import Image

# ==========================================
# 🎨 DESIGN "IMPORTAÇÃO PREMIUM"
# ==========================================
st.set_page_config(page_title="SinoScan", page_icon="🇨🇳", layout="centered")

st.markdown("""
    <style>
    /* Fundo principal do app */
    .stApp {
        background-color: #0b0f19 !important;
    }
    /* Título e textos */
    h1, h2, h3, p, label, .stMarkdown {
        color: #f8fafc !important;
    }
    /* Estilização do Botão Analisar (VERMELHO IMPORTAÇÃO) */
    div.stButton > button:first-child {
        background-color: #e63946 !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        width: 100% !important;
        box-shadow: 0px 4px 15px rgba(230, 57, 70, 0.4) !important;
        font-size: 18px !important;
        margin-top: 20px !important;
    }
    /* Efeito ao clicar no botão */
    div.stButton > button:first-child:hover {
        background-color: #d62828 !important;
        border: none !important;
    }
    /* Caixa de Upload, Inputs e Caixas de Número */
    .stTextInput>div>div>input, .stFileUploader, .stNumberInput>div>div>input {
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

st.title("🇨🇳 Meu Analisador de Anúncios")
st.write("Analise prints de produtos importados com Inteligência Artificial.")

# 1. Entrada da Chave
api_key = st.text_input("Insira sua Gemini API Key:", type="password")

st.write("---")

# 2. SEÇÃO DA CALCULADORA MANUAL (Mantida para simulações adicionais)
st.subheader("📊 Calculadora de Custos Manual (R$)")

col1, col2, col3 = st.columns(3)

with col1:
    valor_produto = st.number_input("Produto:", min_value=0.0, value=0.0)
with col2:
    valor_frete = st.number_input("Frete:", min_value=0.0, value=0.0)
with col3:
    valor_taxa = st.number_input("Taxas:", min_value=0.0, value=0.0)

custo_total = valor_produto + valor_frete + valor_taxa

if custo_total > 0:
    st.markdown(f"""
        <div style="background-color: #1e293b; padding: 15px; border-radius: 8px; border-left: 5px solid #e63946; margin: 15px 0;">
            <p style="margin:0; font-size:12px; color:#94a3b8 !important;">CUSTO TOTAL ESTIMADO (MANUAL):</p>
            <h2 style="margin:0; color:#e63946 !important;">R$ {custo_total:.2f}</h2>
        </div>
    """, unsafe_allow_html=True)

st.write("---")

# 3. SEÇÃO DO PRINT E DA IA COM CONVERSÃO AUTOMÁTICA
st.subheader("🔍 Análise de Viabilidade")
arquivo_image = st.file_uploader("Escolha o print do anúncio:", type=["jpg", "jpeg", "png"])

if arquivo_image:
    imagem = Image.open(arquivo_image)
    st.image(imagem, caption="Imagem carregada para análise", use_container_width=True)

# Turbinando as instruções da IA para caçar os Yuans e converter para Real!
instrucoes = """
Você é um assistente especialista em analisar prints de anúncios de produtos (especialmente de plataformas chinesas de usados como Xianyu).
Olhe atentamente para a imagem e retorne a resposta formatada estritamente em português:

1. DETALHES DO PRODUTO: O nome do produto, marca e especificações encontradas (ex: se é de 64GB, 128GB, 256GB).
2. 💰 VALORES E CONVERSÃO (FAÇA O CÁLCULO): 
   - Identifique o valor do produto exposto em Yuans (¥).
   - Converta esse valor automaticamente para Real Brasileiro (R$) usando uma taxa estimada de R$ 0,80 por Yuan (Multiplique o valor em Yuan por 0.80).
   - Mostre claramente o valor original em Yuan e o valor convertido para Real na resposta (Exemplo: "Valor do Produto: ¥560 (Aprox. R$ 448,00)").
3. INFORMAÇÕES DO VENDEDOR: Olhe no canto superior esquerdo do card do anúncio. Extraia a reputação do vendedor, selos de verificação e há quanto tempo o anúncio foi postado (ex: postado nas últimas 72 horas).
4. VEREDITO FINAL: Diga se com base no preço e no perfil do vendedor o anúncio parece seguro ou se há pontos vermelhos de atenção.
"""

if st.button("Analisar Imagem"):
    if not api_key:
        st.error("Insira a sua API Key primeiro!")
    elif not arquivo_image:
        st.error("Suba uma imagem primeiro!")
    else:
        with st.spinner("Conectando com o servidor de importação e convertendo valores..."):
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
                        st.success("Análise de Importação Concluída com Sucesso!")
                        st.write(texto_analise)
                    except KeyError:
                        st.error("Erro na leitura dos dados da imagem. Tente novamente.")
                else:
                    mensagem_erro = response_data.get('error', {}).get('message', 'Erro desconhecido')
                    st.error(f"Erro: {mensagem_erro}")
                    
            except Exception as e:
                st.error(f"Erro na conexão: {e}")
