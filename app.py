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
                # Conecta com o modelo de visão do Gemini (Flash)
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Envia a foto junto com as instrucoes e mostra o resultado na tela
                resposta = model.generate_content([instrucoes, imagem])
                st.success("Análise Concluída!")
                st.write(resposta.text)
            except Exception as e:
                st.error(f"Erro ao chamar a IA: {e}")
