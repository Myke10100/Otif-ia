import streamlit as st
from openai import OpenAI
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

client = OpenAI(api_key= st.secrets["OPENAI_API_KEY"])

# Cargar la configuración del modelo
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

# Inicializar los mensajes de la conversación
if "messages" not in st.session_state:
    st.session_state.messages = []

# Función para cargar el JSON de gestión de proyectos desde GitHub
@st.cache(ttl=600, allow_output_mutation=True)  # Cache for 10 minutes, allow mutation of the cached result
def load_project_management_info(url):
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()  # Directly return the JSON object
        except json.JSONDecodeError as e:
            st.error(f"Error al decodificar JSON: {e.msg}")
            return None
    else:
        st.error(f"Error al obtener el JSON: {response.status_code}")
        return None

# URL del archivo JSON en GitHub
json_url = "https://raw.githubusercontent.com/Myke10100/Otif-ia/main/dataotif.json"

# Cargar la información del proyecto
project_info = load_project_management_info(json_url)

if project_info:
    st.success("JSON cargado correctamente.")
    st.write("Datos cargados:", project_info)  # Debug: Ver los datos cargados
    # Procesar los datos para contar órdenes por mes, por ejemplo
    orders_by_month = {}
    for item in project_info:
        month = item['Creation Date'].split('-')[1]
        if month in orders_by_month:
            orders_by_month[month] += 1
        else:
            orders_by_month[month] = 1
    st.write("Órdenes por mes:", orders_by_month)  # Debug: Verificar el conteo
else:
    st.error("Error al cargar el JSON.")

# Convertir el JSON en una cadena de texto
project_info_text = json.dumps(project_info, indent=2)

# Crear un prompt inicial personalizado
initial_prompt = (
    # Crear un prompt inicial más simple
initial_prompt = (
    "You are a virtual assistant specialized in OTIF processes. Answer queries directly without showing calculations. "
    "Use the data fields up to April, focusing on practical and easy to understand information."
    "\n\nIf you receive a greeting, respond with: 'Hi, I'm the OTIF Process Specialist Assistant. How can I help you today?'"
    "\n\nAnswer questions clearly and directly, using only the data provided. Do not make assumptions or use examples."
)

# Datos procesados para el prompt (resumidos y específicos para la pregunta)
#data_summary = "Summary of key data fields: PO, Creation Date, Order Value, etc."
#)

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
            response = client.chat.completions.create(model=st.session_state["openai_model"],
            messages=messages)
            response_text = response.choices[0].message.content
        except Exception as e:
            response_text = f"Error al obtener la respuesta de OpenAI: {str(e)}"

        # Mostrar la respuesta del asistente
        st.markdown(response_text)          
    st.session_state.messages.append({"role": "assistant", "content": response_text})












