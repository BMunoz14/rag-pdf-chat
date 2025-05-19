import streamlit as st
from rag import setup_model_and_vectorstore, process_pdf, ask_question
import ollama

st.set_page_config(page_title="RAG para PDF", layout="centered")
st.title("🔍 Chat con tu documento PDF")
st.write("Carga un archivo PDF y haz preguntas sobre su contenido.")

# --- Inicializar historial ---
if "historial" not in st.session_state:
    st.session_state.historial = []

# --- Selección de modelo ---
def list_models():
    models_running = ollama.list()['models']
    return [model["model"] for model in models_running]

lista = list_models()
if 'model_selection' not in st.session_state:
    st.session_state.model_selection = lista[4] if lista else None

# --- Sidebar ---
with st.sidebar:
    st.title('🧠 Opciones')

    st.session_state.model_selection = st.selectbox(
        'Selecciona el modelo:',
        options=lista,
        index=lista.index(st.session_state.model_selection) if st.session_state.model_selection in lista else 0
    )

    uploaded_pdf = st.file_uploader("📄 Carga un PDF", type=["pdf"])
    if uploaded_pdf:
        st.session_state.pdf_path = f"./temp_{uploaded_pdf.name}"
        with open(st.session_state.pdf_path, "wb") as f:
            f.write(uploaded_pdf.read())

    st.session_state.temperature = st.slider('Temperatura', 0.0, 1.0, 0.7, 0.1)
    st.session_state.top_p = st.slider('Top P', 0.0, 1.0, 0.9, 0.1)
    st.session_state.top_k = st.slider('Top K', 0, 100, 40, 1)
    st.session_state.max_tokens = st.slider('Max Tokens', 1, 10000, 10000, 1)
    st.session_state.chunk_size = st.slider('Chunk Size', 100, 3000, 1500, 100)
    st.session_state.chunk_overlap = st.slider('Chunk Overlap', 0, 1000, 300, 50)

# --- Setup modelo y vectorstore ---
llm, vector_store = setup_model_and_vectorstore()

# --- Procesar PDF ---
if 'pdf_path' in st.session_state:
    process_pdf(st.session_state.pdf_path, vector_store)
    st.success("✅ PDF cargado exitosamente.")

# --- Mostrar historial completo ---
for mensaje in st.session_state.historial:
    if mensaje["role"] == "user":
        with st.chat_message("user"):
            st.markdown(mensaje["content"])
    elif mensaje["role"] == "assistant":
        with st.chat_message("ai"):
            st.markdown(mensaje["content"])
            with st.expander("📊 Metadatos de la respuesta"):
                metadata = mensaje.get("metadata", {})
                if metadata:
                    st.write({
                        "Modelo": metadata.get("model", ""),
                        "Tokens del prompt": metadata.get("prompt_eval_count", 0),
                        "Tokens generados": metadata.get("eval_count", 0),
                        "Duración total (s)": round(metadata.get("total_duration", 0) / 1e9, 3),
                        "Razón de finalización": metadata.get("done_reason", ""),
                        "Creado en": metadata.get("created_at", "")
                    })


# --- Entrada del usuario ---
if user_input := st.chat_input("Haz tu pregunta"):
    if 'pdf_path' not in st.session_state:
        st.error("❌ Por favor, carga un documento PDF primero.")
    else:
        with st.chat_message("user"):
            st.markdown(user_input)

        st.session_state.historial.append({
            "role": "user",
            "content": user_input
        })

        with st.spinner("Pensando..."):
            result = ask_question(user_input, llm, vector_store)
            respuesta = result.get("answer", "")
            metadata = result.get("metadata", {})

        with st.chat_message("ai"):
            st.markdown(respuesta)
            with st.expander("📊 Metadatos de la respuesta"):
                if metadata:
                    st.write({
                    "Modelo": metadata.get("model", ""),
                    "Tokens del prompt": metadata.get("prompt_eval_count", 0),
                    "Tokens generados": metadata.get("eval_count", 0),
                    "Duración total (s)": round(metadata.get("total_duration", 0) / 1e9, 3),
                    "Razón de finalización": metadata.get("done_reason", ""),
                    "Creado en": metadata.get("created_at", "")
                    })


        st.session_state.historial.append({
            "role": "assistant",
            "content": respuesta,
            "metadata": metadata
        })
