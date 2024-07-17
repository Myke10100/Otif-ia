import streamlit as st
import openai
import json
import requests
import matplotlib.pyplot as plt

# Configuración básica de la página
st.set_page_config(layout="wide")

# Crear las columnas
col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    st.image("https://res.cloudinary.com/ddmifk9ub/image/upload/v1714666361/OFI/Logos/ofi-black.png")

with col2:
    st.title("Ofi Services support chat")

# Inicializar la clave API de OpenAI directamente desde los secretos
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Cargar la configuración del modelo
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4"

# Inicializar los mensajes de la conversación
if "messages" not in st.session_state:
    st.session_state.messages = []

# Función para cargar el JSON de gestión de proyectos desde GitHub
@st.cache
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
    "Hello, I am the assistant specialized in OTIF related processes. How can I help you today?\n\n"
    f"Additional information:\n{project_info_text}"
)

# Mostrar un mensaje de bienvenida y descripción
if not st.session_state.messages:
    st.session_state.messages.append({"role": "assistant", "content": initial_prompt})

# Mostrar historial de chat
st.header("Virtual Assistant")
for message in st.session_state.messages:
    with st.expander(f"{message['role'].title()} says:"):
        st.markdown(message["content"])

# Manejar la entrada del usuario
user_input = st.text_input("Ask me a question about order management")
if st.button("Send"):
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Llamar a la API de OpenAI para obtener la respuesta
    messages_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
    try:
        response = openai.Completion.create(
            model=st.session_state["openai_model"],
            prompt=messages_text,
            max_tokens=150
        )
        response_text = response.choices[0].text.strip()
        st.session_state.messages.append({"role": "assistant", "content": response_text})

        # Verificar si la respuesta contiene un comando para crear un gráfico
        if "##chart" in response_text:
            # Aquí se crea un gráfico de ejemplo
            fig, ax = plt.subplots()
            ax.plot([1, 2, 3, 4], [10, 20, 25, 30])
            ax.set_title("Sample Chart")
            st.pyplot(fig)
            response_text = response_text.replace("##chart", "")
            st.session_state.messages[-1]["content"] = response_text  # Actualizar el último mensaje

    except Exception as e:
        st.error(f"Error al obtener la respuesta de OpenAI: {str(e)}")










