from pathlib import Path

import streamlit as st

from amanara.rag.chatbot import AmanaraRAG
from amanara.rag.ingestion import IngestionPipeline


def app():

    st.set_page_config(
        page_title="Amanara AI",
        page_icon="assets/logo.png",
        layout="wide",
    )

    @st.cache_resource
    def get_chatbot():
        return AmanaraRAG()

    chatbot = get_chatbot()


    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello! I'm Amanara AI. How can I help you today?",
            }
        ]

    # ---------------- Sidebar ---------------- #

    # with st.sidebar:

    #     st.header("Knowledge Base")

    #     uploaded_file = st.file_uploader(
    #         "Upload PDF or TXT",
    #         type=["pdf", "txt"],
    #     )

    #     if uploaded_file is not None:

    #         kb_path = Path("knowledge_base")
    #         kb_path.mkdir(exist_ok=True)

    #         file_path = kb_path / uploaded_file.name

    #         with open(file_path, "wb") as f:
    #             f.write(uploaded_file.getbuffer())

    #         st.success(f"{uploaded_file.name} uploaded successfully!")

    #     if st.button("🔄 Rebuild Knowledge Base"):

    #         with st.spinner("Rebuilding knowledge base..."):

    #             pipeline = IngestionPipeline()
    #             pipeline.run()

    #         st.success("Knowledge base rebuilt successfully!")

    with st.sidebar:
        st.header("Knowledge Base")

        st.success("Knowledge Base Loaded")

        st.info(
            "This chatbot uses a curated Amanara knowledge base."
        )

    # ---------------- Main Page ---------------- #

    col1, col2 = st.columns([1, 6])

    with col1:
        st.image("assets/logo.png", width=80)

    with col2:
        st.title("Amanara AI")

    st.caption("Ask questions about Amanara Solar.")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask your question...")

    if question:


        st.session_state.messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        with st.chat_message("user"):
            st.markdown(question)


        with st.spinner("Searching knowledge base..."):
            

            try:
                result = chatbot.ask(
                    question,
                st.session_state.messages,
            )

            except Exception:
                st.error("An unexpected error occurred while generating the response.")
                raise
                st.stop()


            answer = result["answer"]
            sources = result["sources"]


        with st.chat_message("assistant"):
            st.markdown(answer)

            if sources:
                st.divider()
                st.markdown("**📄 Sources**")

                displayed_sources = set()

                for chunk in sources:
                    payload = chunk.payload or {}

                    source_name = Path(
                        payload.get("source", "Unknown")
                    ).name

                    if source_name not in displayed_sources:
                        st.markdown(f"- {source_name}")
                        displayed_sources.add(source_name)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

