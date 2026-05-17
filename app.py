import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configura o visual da página do seu app
st.title("🔍 Meu Analisador de Anúncios")
st.write("Faça o upload do print do anúncio para analisar os detalhes.")

# 2. Campo para colar a chave de acesso da IA
api_key = st.text_input("Insira sua Gemini API Key:", type="password")

# 3. Campo para subir a foto ou print do celular
arquivo_image = st.file_uploader("Escolha o print do anúncio:", type=["jpg", "jpeg", "png"])

if arquivo_image:
    imagem = Image.open(arquivo_image)
    st.image(imagem, caption="Imagem carregada", use_container_width=True)

# 4. As instruções secretas (Prompt) que a IA vai seguir ao ler a foto
instrucoes = """
Você é um assistente especialista em analisar prints de anúncios de produtos (como roupas e tênis).
Olhe para a imagem e retorne:
1. O nome do produto e a marca.
2. O preço estimado.
3. Se o anúncio parece confiável ou se há pontos de atenção.
"""

# 5. Botão que aciona a Inteligência Artificial
if st.button("Analisar Imagem"):
    if not api_key:
        st.error("Insira a sua API Key primeiro!")
    elif not arquivo_image:
        st.error("Suba uma imagem primeiro!")
    else:
        with st.spinner("Analisando..."):
            try:
                # Configura a chave de acesso no pacote antigo
                genai.configure(api_key=api_key)
                
                # Força o uso do modelo de visão clássico da biblioteca antiga
                model = genai.GenerativeModel('gemini-pro-vision')
                
                # Envia os dados no formato que o servidor antigo entende
                resposta = model.generate_content([instrucoes, imagem])
                st.success("Análise Concluída!")
                st.write(resposta.text)
            except Exception as e:
                # Se o modelo antigo reclamar, tentamos o plano B automático
                try:
                    model_flash = genai.GenerativeModel('gemini-1.5-flash')
                    resposta = model_flash.generate_content([instrucoes, imagem])
                    st.success("Análise Concluída!")
                    st.write(resposta.text)
                except Exception as erro_b:
                    st.error(f"Erro ao chamar a IA: {e} | Plano B: {erro_b}")
