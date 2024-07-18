import streamlit as st
import json
import requests
import matplotlib.pyplot as plt
import numpy as np
from openai import OpenAI

# Configuración de la API de OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Configuración básica de la página
st.set_page_config(layout="wide")

# Crear las columnas para el layout
col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    st.image("https://res.cloudinary.com/ddmifk9ub/image/upload/v1714666361/OFI/Logos/ofi-black.png")

with col2:
    st.title("Ofi Services Support Chat")

# Cargar y decodificar JSON desde GitHub
@st.experimental_memo
def load_project_management_info(url):
    response = requests.get(url)
    if response.status_code != 200:
        st.error(f"Error al obtener el JSON: {response.status_code}")
        return {}
    return response.json()

json_url = "https://raw.githubusercontent.com/Myke10100/Otif-ia/main/dataotif.json"
project_info = load_project_management_info(json_url)

# Inicializar mensajes de la conversación
if "messages" not in st.session_state:
    st.session_state.messages = []

# Generación de prompt inicial
initial_prompt = f"""Hello, I'm the OTIF Process Specialist Assistant. How can I help you today?\n\n{json.dumps(project_info, indent=2)}"""

# Mostrar mensaje de bienvenida
if not st.session_state.messages:
    st.session_state.messages.append({"role": "system", "content": initial_prompt})

# Mostrar historial de chat
st.header("Virtual Assistant Chat")
for message in st.session_state.messages:
    role = "user" if message["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(message["content"])

# Entrada de usuario
user_input = st.text_input("Ask me a question about order management")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    response = client.Completion.create(
        model=st.session_state.get("openai_model", "gpt-4o"),
        prompt=user_input,
        max_tokens=150
    )
    response_text = response.choices[0].text.strip()
    st.session_state.messages.append({"role": "assistant", "content": response_text})

    # Generar y mostrar gráficos si es pertinente
    if "graph" in response_text.lower():
        # Simulación de datos para el ejemplo
        data = np.random.randn(10)
        plt.figure(figsize=(10, 4))
        plt.plot(data)
        plt.title('Ejemplo de Gráfico')
        plt.xlabel('Tiempo')
        plt.ylabel('Valor')
        st.pyplot(plt)












