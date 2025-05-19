📄 RAG con Streamlit y Ollama

Este proyecto permite cargar documentos PDF y hacerles preguntas utilizando un enfoque de RAG (Retrieval-Augmented Generation), todo dentro de una interfaz conversacional tipo ChatGPT construida con Streamlit.

🚀 Características
- Carga dinámica de archivos PDF.
- Extracción de texto y segmentación en chunks configurables.
- Recuperación semántica con vectores (Chroma + embeddings de Ollama).
- Generación de respuestas con modelos locales a través de Ollama.

🧱 Estructura del proyecto
RAG/
├── src/
│   ├── app.py         # Interfaz Streamlit principal
│   └── rag.py         # Lógica de RAG: embeddings, recuperación, generación
├── data/
│   ├── documento.pdf  # Documento PDF de prueba
├── .venv/             # Entorno virtual (opcional)
├── chroma_langchain_db/ # Persistencia del vector store (se crea al correr)
├── pyproject.toml     # Dependencias del proyecto
├── gitignore
└── README.md          # Este archivo

⚙️ Requisitos y dependencias necesarias
Lee las dependencias que están en el documento pyproject.toml
y utilizando uv puedes agregarlas a tu entorno virtual con los comandos "uv add [dependencia]"
con eso ya tienes todas tus dependencias al día.

▶ Cómo ejecutar la aplicación
Desde la raíz del proyecto:
solo escribe "make stream" y listo tendrás tu agente RAG disponible para preguntar sobre tu documento PDF
(Esto abrirá automáticamente la interfaz en tu navegador).

🧠 ¿Cómo usarlo?
En la barra lateral, carga tu documento PDF.
- Ajusta parámetros como:
- Chunk size y overlap
- Temperatura, top-k, top-p, max tokens
- Escribe tu pregunta en el chat.
La respuesta aparecerá y ouedes hacer múltiples preguntas sobre el mismo PDF.

🧪 Notas adicionales
- Este proyecto no usa la nube: todo corre localmente.
- Requiere una máquina con suficiente RAM para usar modelos grandes como llama3.
- Puedes extenderlo para múltiples archivos, búsqueda cruzada, o integración con bases de conocimiento.

🙌 Créditos
Desarrollado como una base práctica para experimentación con Retrieval-Augmented Generation (RAG) local utilizando LangChain, Streamlit y Ollama.