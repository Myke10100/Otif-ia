import streamlit as st
import openai
import json
import requests

# Set up the page configuration
st.set_page_config(layout="wide")


# Crear las columnas
col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    st.image("https://res.cloudinary.com/ddmifk9ub/image/upload/v1714666361/OFI/Logos/ofi-black.png")

with col2:
    st.title("Chat de asistencia Ofi Services")

#with col3:
   #st.image("https://brandworld.ab-inbev.com/sites/g/files/wnfebl3996/files/Style%20Guide/MicrosoftTeams-image%20%282%29.png")


openai.api_key = "sk-proj-IXnNYf0z335ehaLHFAUST3BlbkFJ9qDdxQYNIrc4vMmZE6rz"

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

# Convertir el JSON en una cadena de texto
project_info_text = json.dumps(project_info, indent=2)

# Crear un prompt inicial personalizado
initial_prompt = (
    " Usted es un asistente de datos con amplios conocimientos especializado en logística, gestión de la cadena de suministro y procesos de cuentas por pagar. Tienes acceso a un conjunto de datos "
    " que contiene información detallada sobre las órdenes de pedido, su estado, materiales, informacion de creditos y diversas métricas logísticas. Este conjunto de datos incluye "
    "columnas como:\n"
    "PV\n"
    "FECHA CREACIÓN\n"
    "VALOR PV\n"
    "MATERIAL\n"
    "NEGOCIO\n"
    "CLIENTE\n"
    "CANTIDAD"
    "LÍMITE DE CRÉDITO\n"
    "CRÉDITO USADO\n"
    "% CRÉDITO USADO\n"
    "NUMERO DE ENTREGA\n"
    "FECHA COMPROMISO ENTREGA\n"
    "FECHA ENTREGA\n"
    "ESTADO\n\n"
    f"{project_info_text}\n\n"
    "Si recibe un saludo como 'hola' o 'hola', preséntese diciendo: 'Hola, soy el asistente especializado en logística, gestión de la cadena de suministro. ¿En qué puedo ayudarle hoy?'\n"
    "Por favor, responda a las preguntas de forma clara y directa, evitando la jerga técnica y centrándose en información práctica y fácil de entender basada en el conjunto de datos proporcionado.")

# Show a welcome message and description
if not st.session_state.messages:
    st.session_state.messages.append({"role": "system", "content": initial_prompt})
    with st.chat_message("assistant"):
        st.markdown("I am a virtual MAZ Continuous Improvement Assistant")

# Display chat history
st.header("Chat History")
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
    elif message["role"] == "assistant":
        with st.chat_message("assistant"):
            st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Ask me a question about project management"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)


    # Llamar a la API de OpenAI para obtener la respuesta
    with st.chat_message("assistant"):
        messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        response = openai.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=messages
        )
        response_text = response.choices[0].message.content
        # Mostrar la respuesta del asistente
        st.markdown(response_text)
    st.session_state.messages.append({"role": "assistant", "content": response_text})
