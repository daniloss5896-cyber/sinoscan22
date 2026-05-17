import streamlit as st
import requests
import base64
from PIL import Image
import io

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

# 5. Botão que aciona a Inteligência Artificial via Requisição Direta
if st.button("Analisar Imagem"):
    if not api_key:
        st.error("Insira a sua API Key primeiro!")
    elif not arquivo_image:
        st.error("Suba uma imagem primeiro!")
    else:
        with st.spinner("Analisando diretamente nos servidores do Google..."):
            try:
                # Converte a imagem carregada para bytes e depois para Base64 (formato seguro para envio)
                bytes_data = arquivo_image.getvalue()
                base64_image = base64.b64encode(bytes_data).decode('utf-8')
                mime_type = arquivo_image.type

                # Monta a URL de conexão direta com a API oficial e moderna do Gemini (v1)
                url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash-latest:generateContent?key={api_key}"

                
                # Configura o cabeçalho padrão da internet
                headers = {'Content-Type': 'application/json'}
                
                # Monta os dados com as instruções e a imagem em Base64
                payload = {
                    "contents": [{
                        "parts": [
                            {"text": instrucoes},
                            {
                                "inlineData": {
                                    "mimeType": mime_type,
                                    "data": base64_image
                                }
                            }
                        ]
                    }]
                }
                
                # Faz o envio direto para o Google
                response = requests.post(url, headers=headers, json=payload)
                response_data = response.json()
                
                # Verifica se o Google respondeu com sucesso
                if response.status_code == 200:
                    try:
                        texto_analise = response_data['candidates'][0]['content']['parts'][0]['text']
                        st.success("Análise Concluída com Sucesso!")
                        st.write(texto_analise)
                    except KeyError:
                        st.error("A IA respondeu, mas o formato veio inesperado. Tente novamente.")
                else:
                    mensagem_erro = response_data.get('error', {}).get('message', 'Erro desconhecido')
                    st.error(f"Erro no servidor do Google: {mensagem_erro}")
                    
            except Exception as e:
                st.error(f"Erro na conexão direta: {e}")
