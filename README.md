📄 RAG con Streamlit y Ollama

Este proyecto permite cargar documentos PDF y hacerles preguntas utilizando un enfoque de RAG (Retrieval-Augmented Generation), todo dentro de una interfaz conversacional tipo ChatGPT construida con Streamlit.

🚀 Características

Carga dinámica de archivos PDF.

Extracción de texto y segmentación en chunks configurables.

Recuperación semántica con vectores (Chroma + embeddings de Ollama).

Generación de respuestas con modelos locales como llama3 a través de Ollama.

Visualización de historial conversacional.

Visualización de metadatos detallados de cada respuesta (tokens, duración, modelo, etc).

🧱 Estructura del proyecto

RAG/
├── src/
│   ├── app.py         # Interfaz Streamlit principal
│   └── rag.py         # Lógica de RAG: embeddings, recuperación, generación
├── .venv/             # Entorno virtual (opcional)
├── chroma_langchain_db/ # Persistencia del vector store (se crea al correr)
├── requirements.txt   # Dependencias del proyecto
└── README.md          # Este archivo

⚙️ Requisitos

Python 3.10+

Ollama instalado y corriendo

Modelos como llama3 y nomic-embed-text descargados en Ollama

Instala las dependencias:

pip install -r requirements.txt

Ejecuta Ollama en segundo plano (si no está activo):

ollama run llama3
ollama run nomic-embed-text

▶ Cómo ejecutar la aplicación

Desde la raíz del proyecto:

streamlit run src/app.py

Esto abrirá automáticamente la interfaz en tu navegador (por defecto: http://localhost:8501).

🧠 ¿Cómo usarlo?

En la barra lateral, carga tu documento PDF.

Ajusta parámetros como:

Chunk size y overlap

Temperatura, top-k, top-p, max tokens

Escribe tu pregunta en el chat.

La respuesta aparecerá junto con sus metadatos dentro de un expander.

Puedes hacer múltiples preguntas sobre el mismo PDF y revisar todo el historial de interacción.

📦 Dependencias principales

streamlit

langchain

langchain-community

langchain-chroma

langgraph

ollama

python-dotenv

🛠 Personalización

Para cambiar el modelo por defecto, modifica model_name en setup_model_and_vectorstore().

Para cambiar el prompt base, modifica prompt = hub.pull(...) en rag.py.

Puedes almacenar múltiples historiales, exportarlos o integrar autenticación.

🧪 Notas adicionales

Este proyecto no usa la nube: todo corre localmente.

Requiere una máquina con suficiente RAM para usar modelos grandes como llama3.

Puedes extenderlo para múltiples archivos, búsqueda cruzada, o integración con bases de conocimiento.

🙌 Créditos

Desarrollado como una base práctica para experimentación con Retrieval-Augmented Generation (RAG) local utilizando LangChain, Streamlit y Ollama.