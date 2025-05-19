import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain import hub
from langgraph.graph import START, StateGraph
from langchain_core.documents import Document
from typing_extensions import TypedDict, List
import streamlit as st

# --- Configuración inicial ---
load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"]  = "true"
os.environ["LANGCHAIN_API_KEY"]     = os.getenv("LANGCHAIN_API_KEY")
os.environ["USER_AGENT"]            = "AgenteUAO"
os.environ["LANGCHAIN_PROJECT"]     = "OllamaRAG_V2"

# --- Inicializar prompt ---
prompt = hub.pull("rlm/rag-prompt")

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str

# --- Configurar modelo y vectorstore ---
def setup_model_and_vectorstore():
    llm = ChatOllama(
        model=st.session_state.model_selection,
        temperature=st.session_state.temperature,
        top_p=st.session_state.top_p,
        top_k=st.session_state.top_k,
        num_predict=st.session_state.max_tokens,
    )

    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vector_store = Chroma(
        collection_name="pdf_collection",
        embedding_function=embeddings,
        persist_directory="./chroma_langchain_db",
    )

    return llm, vector_store

# --- Procesar el PDF cargado ---
def process_pdf(pdf_path: str, vector_store):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=st.session_state.get("chunk_size", 1500),
        chunk_overlap=st.session_state.get("chunk_overlap", 300)
    )
    chunks = text_splitter.split_documents(docs)
    vector_store.reset_collection()
    vector_store.add_documents(chunks)

# --- Recuperar contexto ---
def retrieve_context(state: State, vector_store):
    question = state["question"]
    return {"context": vector_store.similarity_search(question, k=5)}

# --- Generar respuesta ---
def generate_answer(state: State, llm):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    history = "\n".join([
        f"Usuario: {msg['content']}" if msg['role'] == 'user' else f"Asistente: {msg['content']}"
        for msg in st.session_state.get("historial", [])
    ])
    full_context = f"{history}\n\n{docs_content}"

    messages = prompt.invoke({"question": state["question"], "context": full_context})
    response = llm.invoke(messages)

    metadata = {}
    if hasattr(response, "response_metadata") and isinstance(response.response_metadata, dict):
        metadata = response.response_metadata.copy()

    return {
        "answer": response.content,
        "metadata": metadata
    }

# --- Construcción del grafo y ejecución ---
def ask_question(raw_question: str, llm, vector_store):
    graph_builder = StateGraph(State)
    graph_builder.add_node("retrieve_context", lambda state: retrieve_context(state, vector_store))
    graph_builder.add_node("generate_answer", lambda state: generate_answer(state, llm))
    graph_builder.add_edge(START, "retrieve_context")
    graph_builder.add_edge("retrieve_context", "generate_answer")
    graph = graph_builder.compile()

    result = graph.invoke({"question": raw_question})
    return {
        "answer": result["answer"],
        "metadata": result.get("metadata", {})
    }

