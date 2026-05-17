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
        with st.spinner("Analisando com o motor do Gemini..."):
            try:
                # 1. Configura a chave de acesso usando o cliente moderno do pacote instalado
                genai.configure(api_key=api_key)
                
                # 2. Força o uso do modelo estável de produção
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                # 3. Faz a chamada passando o texto e a imagem em formato PIL diretamente
                resposta = model.generate_content([instrucoes, imagem])
                
                if resposta.text:
                    st.success("Análise Concluída com Sucesso!")
                    st.write(resposta.text)
                else:
                    st.warning("A IA processou, mas não gerou texto. Tente novamente.")
                    
            except Exception as e:
                # PLANO B DE EMERGÊNCIA: Se a biblioteca principal der ruim, usamos o modelo antigo de fallback
                try:
                    model_backup = genai.GenerativeModel("gemini-pro-vision")
                    resposta_backup = model_backup.generate_content([instrucoes, imagem])
                    st.success("Análise Concluída pelo Modo de Segurança!")
                    st.write(resposta_backup.text)
                except Exception as erro_b:
                    st.error(f"Erro no motor principal: {e}")
                    st.error(f"Erro no motor de segurança: {erro_b}")
                    st.info("Dica: Verifique se sua API Key foi copiada corretamente e não possui espaços.")
