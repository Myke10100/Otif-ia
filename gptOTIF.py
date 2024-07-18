import streamlit as st
import json
import requests
import matplotlib.pyplot as plt
from openai import OpenAI

# Configuración de la API de OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Configuración básica de la página
st.set_page_config(layout="wide")

# Crear las columnas
col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    st.image("https://res.cloudinary.com/ddmifk9ub/image/upload/v1714666361/OFI/Logos/ofi-black.png")

with col2:
    st.title("Ofi Services Support Chat")

# Cargar la información de GitHub
@st.experimental_memo
def load_project_management_info(url):
    response = requests.get(url)
    if response.status_code != 200:
        st.error(f"Error al obtener el JSON: {response.status_code}")
        st.stop()
    return response.json()

json_url = "https://raw.githubusercontent.com/Myke10100/Otif-ia/main/dataotif.json"
project_info = load_project_management_info(json_url)

# Inicializar mensajes de la conversación
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Mostrar mensaje de bienvenida
initial_prompt = "Hello, I'm the OTIF Process Specialist Assistant. How can I help you today?"
if not st.session_state["messages"]:
    st.session_state["messages"].append({"role": "system", "content": initial_prompt})

# Mostrar historial de chat
st.header("Virtual Assistant Chat")
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Manejar la entrada del usuario
user_input = st.text_input("Ask me a question about order management")
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state["messages"]]
    response = client.chat.completions.create(
        model=st.session_state.get("openai_model", "gpt-4o"),
        messages=messages
    )
    response_text = response.choices[0].message["content"]
    st.session_state["messages"].append({"role": "assistant", "content": response_text})

    # Generar gráfico si es necesario
    if "graph" in response_text.lower():  # Puedes ajustar la condición para detectar necesidad de gráfico
        data = [float(s) for s in response_text.split() if s.isdigit()]  # Suposición de cómo se extraen los datos
        plt.figure(figsize=(10, 5))
        plt.plot(data)
        plt.title("Generated Graph")
        plt.xlabel("Index")
        plt.ylabel("Value")
        st.pyplot(plt)

# Actualización del estado
#if st.session_state["messages"]:
 #   st.experimental_rerun()












