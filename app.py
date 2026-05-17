import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuração da página
st.title("🔍 Meu Analisador de Anúncios")
st.write("Faça o upload do print do anúncio para analisar os detalhes.")

# Entrada da chave
api_key = st.text_input("Insira sua Gemini API Key:", type="password")

# Upload da imagem
arquivo_image = st.file_uploader("Escolha o print do anúncio:", type=["jpg", "jpeg", "png"])

if arquivo_image:
    imagem = Image.open(arquivo_image)
    st.image(imagem, caption="Imagem carregada", use_container_width=True)

# Instruções para a IA
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
        with st.spinner("Analisando..."):
            try:
                # 1. Configura a chave de acesso
                genai.configure(api_key=api_key)
                
                # 2. ESSA LINHA É O SEGREDO: Força o cliente a ignorar a v1beta e usar a v1 estável
                client_options = {"api_version": "v1"}
                
                # 3. Inicializa o modelo com a versão correta de produção
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    client_options=client_options
                )
                
                # 4. Envia os dados
                resposta = model.generate_content([instrucoes, imagem])
                
                if resposta.text:
                    st.success("Análise Concluída!")
                    st.write(resposta.text)
                else:
                    st.warning("O modelo não retornou texto. Tente novamente.")
                    
            except Exception as e:
                st.error(f"Erro no processamento: {e}")
