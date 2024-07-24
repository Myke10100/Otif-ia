import streamlit as st
from openai import OpenAI
import pandas as pd
import json
import requests

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

# Acceder a la clave API de OpenAI directamente
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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
        return response.json()
    except json.JSONDecodeError as e:
        st.error(f"Error al decodificar JSON: {e.msg}")
        st.stop()

# URL del archivo JSON en GitHub
json_url = "https://raw.githubusercontent.com/Myke10100/Otif-ia/main/dataotif.json"

# Cargar la información del proyecto
project_info = load_project_management_info(json_url)

# Convertir el JSON en una cadena de texto para el prompt
project_info_text = json.dumps(project_info, indent=2)

# Crear un prompt inicial personalizado
initial_prompt = (
    "You will be a virtual assistant who will act as a specialized consultant, with high knowledge in analysis related to OTIF processes."
    "You are a virtual assistant, who will answer questions like CHAT GPT, in the answers you should not see formulas, nor formulas, nor where you take the data, only short and specific answers, the calculations will be done with the following fields, but remember this should not be shown as a result."
    "Columns with data up to April remember, take unique values, do not duplicate any information the date format is DD-MM-YYYYYY keep in mind the amount of orders per month, and that this is proportional to the total amount of orders of all the data, retify the information very well to avoid quantity errors.\n"
    "PO\n"
    "Creation Date\n"
    "Order Value\n"
    "Material\n"
    "Business Unit\n"
    "Client\n"
    "Committed Quantity\n"
    "Actual Delivered Quantity\n"
    "Credit Limit\n"
    "Accumulated Credit used\n"
    "Credit used by order (%)\n"
    "Committed Delivery Date\n"
    "Actual Delivery Date\n"
    "Reason for Delay\n"
    "Supplier\n"
    "Warehouse Location\n"
    "Order Priority\n"
    "Delivery Delay (Days)\n"
    "On Time\n"
    "In Full\n"
    "Reasons for Delay On Time/Days\n"
    "Reasons for Delay In Full/ Days\n\n"
    f"{project_info_text}\n\n"
    "If you receive a “hello” or “hi” greeting, introduce yourself by saying, “Hi, I'm the OTIF Process Specialist Assistant. How can I help you today?"
    "Answer questions clearly and directly according to previous information, DO NOT MAKE ASSUMPTIONS, DO NOT USE EXAMPLES, DO NOT SHOW CALCULATIONS OR FORMULAS, use 100% of the data provided, avoid at all costs giving details of analysis and technical data, focus on practical and easy to understand information, remember that you are a consultant must give short and clear answers.")

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
            response = client.chat.completions.create(
                model=st.session_state["openai_model"],
                temperature=0.1,  # Temperatura mínima
                max_tokens=500  # Máximo de 500 tokens
                messages=messages
            )
            response_text = response.choices[0].message.content
        except Exception as e:
            response_text = f"Error al obtener la respuesta de OpenAI: {str(e)}"

        # Mostrar la respuesta del asistente
        st.markdown(response_text)
    st.session_state.messages.append({"role": "assistant", "content": response_text})










