import streamlit as st
from openai import OpenAI
import pandas as pd
import json
import requests

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Configuración básica de la página
st.set_page_config(layout="wide")

# Crear las columnas
col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    st.image("https://res.cloudinary.com/ddmifk9ub/image/upload/v1714666361/OFI/Logos/ofi-black.png")

with col2:
    st.title("Ofi Services support chat")

with col3:
    st.image("https://upload.wikimedia.org/wikipedia/commons/0/0c/AkzoNobel_logo.png")

# Cargar la configuración del modelo
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

# Inicializar los mensajes de la conversación
if "messages" not in st.session_state:
    st.session_state.messages = []

# Función para cargar el JSON de gestión de proyectos desde GitHub
@st.cache_data
def load_project_management_info(url):
    response = requests.get(url)
    if response.status_code != 200:
        st.error(f"Error al obtener el JSON: {response.status_code}")
        st.stop()

    try:
        data = response.json()
        # Validar la estructura del JSON
        if not isinstance(data, list) or not all(isinstance(d, dict) for d in data):
            raise ValueError("La estructura del JSON no es la esperada.")
        return data
    except (json.JSONDecodeError, ValueError) as e:
        st.error(f"Error al decodificar o validar JSON: {str(e)}")
        st.stop()

# URL del archivo JSON en GitHub
json_url = "https://raw.githubusercontent.com/Myke10100/Otif-ia/main/dataotif.json"

# Cargar la información del proyecto
project_info = load_project_management_info(json_url)

# Convertir el JSON en una cadena de texto
project_info_text = json.dumps(project_info, indent=2)

# Crear un prompt inicial personalizado
initial_prompt = (
    "You will be a virtual assistant who will act as a specialized consultant with high knowledge in analysis related to OTIF processes. "
    "You will answer questions like ChatGPT, but in your answers, you should not show formulas, calculations, or where you took the data from. Only provide short and specific answers. "
    "The calculations will be done with the following fields, but remember these should not be shown as a result:\n\n"
    "Columns with data up to June, remember to take the unique values, do not duplicate any information:\n"
    "- PO\n"
    "- Creation Date\n"
    "- Order Value\n"
    "- Material\n"
    "- Business Unit\n"
    "- Client\n"
    "- Committed Quantity\n"
    "- Actual Delivered Quantity\n"
    "- Credit Limit\n"
    "- Accumulated Credit used\n"
    "- Credit used by order (%)\n"
    "- Committed Delivery Date\n"
    "- Actual Delivery Date\n"
    "- Supplier\n"
    "- Warehouse Location\n"
    "- Order Priority\n"
    "- Delivery Delay (Days)\n"
    "- On Time\n"
    "- In Full\n"
    "- Reasons for Delay On Time/Days\n"
    "- Reasons for Delay In Full/ Days\n\n"
    f"{project_info_text}\n\n"
    "If you receive a “hello” or “hi” greeting, introduce yourself by saying, “Hi, I'm the OTIF Process Specialist Assistant. How can I help you today?”\n"
    "Answer questions clearly and directly according to previous information. DO NOT MAKE ASSUMPTIONS, DO NOT USE EXAMPLES, DO NOT SHOW CALCULATIONS OR FORMULAS. "
    "Use 100% of the data provided and avoid at all costs giving details of analysis and technical data. Focus on practical and easy-to-understand information. "
    "Remember that as a consultant, you must give short and clear answers."
)

# Mostrar un mensaje de bienvenida y descripción
if not st.session_state.messages:
    st.session_state.messages.append({"role": "system", "content": initial_prompt})
    with st.chat_message("assistant"):
        st.markdown("Hello, I am the assistant specialized in OTIF related processes, how can I help you today?")

# Mostrar historial de chat
st.header("Virtual Assistant")
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(message["content"])

# Manejar la entrada del usuario
if prompt := st.chat_input("Ask me a question about order management"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Llamar a la API de OpenAI para obtener la respuesta
    with st.chat_message("assistant"):
        messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        try:
            response = client.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=messages
            )
            response_text = response.choices[0].message["content"]
        except Exception as e:
            response_text = f"Error al obtener la respuesta de OpenAI: {str(e)}"

        # Mostrar la respuesta del asistente
        st.markdown(response_text)
    st.session_state.messages.append({"role": "assistant", "content": response_text})










