import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stodo import to_do
from streamlit_extras.mention import mention
from st_pages import Page, show_pages, add_page_title
import requests  # Importando la biblioteca de requests
import json

show_pages(
    [
        Page("other_pages/️empresa.py", "Admin", ":gear:"),
    ]
)

add_page_title("Anahuac Copilot", page_icon="🤖")


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True


if check_password():

    # Instrucciones en la sidebar
    st.sidebar.image("resources/VHuman.webp", width=200)
    st.sidebar.markdown("""
    ### Instrucciones:
    1. **Analíticas:** Consulta tus métricas de uso.
    2. **Chats:** Interactúa con la inteligencia artificial.
    3. **Configuración:** Ajusta los parámetros de tu chatbot.
    4. **Conexiones:** Integra con tus redes sociales preferidas.
    """)

    # Opción para navegación por pestañas en la sidebar
    option = st.sidebar.selectbox("Menú", ["Analíticas", "Chats", "Configuración", "Conexiones"])

    if option == "Analíticas":
        import streamlit as st
    import requests

    # Dirección del endpoint
    end_point_metrics = "http://ec2-18-191-126-188.us-east-2.compute.amazonaws.com:5000/metrics"


    def fetch_metrics():
        resp = requests.get(end_point_metrics)
        return resp.json()


    if option == "Analíticas":
        try:

            # Recuperar las métricas desde el backend
            metrics = fetch_metrics()
            st.title("Analíticas")
            st.write("Aquí puedes consultar las métricas relacionadas con el uso de la aplicación.")

            # Estas líneas asumen que sólo te importa el dato del día actual. Si quieres mostrar datos de múltiples fechas, deberás ajustar este código.
            tokens_used_today = metrics['total_tokens_input'].get("09_08_2023", 0) + metrics['total_tokens_output'].get(
                "09_08_2023", 0)
            tokens_available = 100000 - tokens_used_today  # Asume que tienes 100000 tokens como límite

            col1, col2, col3 = st.columns(3)
            col1.metric(label="Tokens Usados", value=tokens_used_today)
            col2.metric(label="Tokens Disponibles", value=tokens_available)
            # El valor y el delta de "Conversaciones 24/h" son estáticos en tu ejemplo, así que lo dejé igual:
            # Estilo para las tarjetas de métricas
            # Si tienes una función específica para dar estilo, puedes llamarla aquí.
            # Sin embargo, no proporcionaste la definición exacta de "style_metric_cards", así que la línea siguiente es un placeholder.
            # style_metric_cards(border_left_color="blue-70 ")
            style_metric_cards(border_left_color="orange")
        except Exception as e:
            print("An error ocurred :", str(e))
            st.error("Issues connecting to the server!")


    elif option == "Chats":
        st.title("Chats")
        st.write("Interactúa directamente con la inteligencia artificial. Pronto habrá una caja de chat aquí.")
        end_point_conversations = "http://127.0.0.1:8000/get_conversations"


        def fetch_conversations():
            try:
                resp = requests.get(end_point_conversations)
                return json.loads(resp.text)
            except Exception as e:
                print("An error ocurred :", str(e))
                st.error("Issues connecting to the server!")


        def display_conversation(conversation_id):
            convo = conversations[conversation_id]
            for msg in convo:
                role = msg["role"]
                content = msg["content"]
                if role == "user":
                    with st.chat_message(name="user"):
                        st.write(content)
                elif role == "assistant":
                    with st.chat_message(name="assistant", avatar="resources/AI.png"):
                        st.write(content)
                else:  # System messages or other type of roles
                    st.write(f"({role}): {content}")


        conversations = fetch_conversations()

        if conversations:
            # Create tabs for each conversation ID
            tab = st.selectbox("Selecciona una conversación:", list(conversations.keys()))

            st.subheader(f"Conversación ID: {tab}")
            display_conversation(tab)

            st.write("\n\n")
            st.markdown("[Desarrollado por VHuman.ai](https://Vhuman.ai)")
        else:
            st.error("No se pudo cargar las conversaciones.")

    elif option == "Configuración":
        st.title("Configuración")
        st.write("Ajusta los parámetros y preferencias para tu chatbot de atención al cliente.")
        try:

            # Obtener el prompt desde el servidor
            response = requests.get("http://ec2-18-191-126-188.us-east-2.compute.amazonaws.com:5000/prompt")
            if response.status_code == 200:
                current_prompt = response.json().get('prompt', '')
            else:
                current_prompt = ''

            prompt = st.text_input("Prompt", current_prompt)
            uploaded_file = st.file_uploader("Conocimiento Empresa (solo PDF)", type=["pdf"])

            if st.button("Enviar"):
                # Actualizar el prompt en el servidor
                response_prompt = requests.post("http://ec2-18-191-126-188.us-east-2.compute.amazonaws.com:5000/prompt", json={"prompt": prompt})

                # Envía el archivo si ha sido cargado
                if uploaded_file:
                    response_knowledge = requests.post("http://ec2-18-191-126-188.us-east-2.compute.amazonaws.com:5000/knowledge", files={"files": uploaded_file})

                    if response_knowledge.status_code != 200:
                        st.error(
                            "Error al subir el archivo: " + response_knowledge.json().get('error', 'Unknown error'))

                if response_prompt.status_code == 200:
                    st.success("Configuración guardada con éxito!")
                    st.balloons()
                else:
                    st.error("Error al actualizar la configuración")
        except Exception as e:
            print("An error ocurred :", str(e))
            st.error("Issues connecting to the server!")

    elif option == "Conexiones":
        st.title("Proximamente")

mention(
    label="Desarrollado por VHuman.ai",
    url="https://Vhuman.ai",
)
