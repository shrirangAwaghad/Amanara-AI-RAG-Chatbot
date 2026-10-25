
import streamlit as st
from pathlib import Path
from amanara.rag.chatbot import AmanaraRAG

# --------------------------------------------------
# Page configuration
# --------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[3]
LOGO_PATH = PROJECT_ROOT / "assets" / "logo.png"

st.set_page_config(
    page_title="Amanara AI Chatbot",
    page_icon=str(LOGO_PATH) if LOGO_PATH.exists() else "â˜€ï¸",
    layout="centered",
)

# --------------------------------------------------
# Simple white theme with subtle green accents
# --------------------------------------------------
st.markdown(
    """
    <style>
        /* Main page */
        .stApp {
            background-color: #FFFFFF;
            color: #1F2937;
        }

        [data-testid="stHeader"] {
            background-color: #FFFFFF;
        }

        .block-container {
            max-width: 850px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        /* Headings and general text */
        h1, h2, h3, p, label,
        [data-testid="stMarkdownContainer"],
        [data-testid="stCaptionContainer"] {
            color: #1F2937;
        }

        .amanara-subtitle {
            color: #4B5563 !important;
            font-size: 1rem;
            margin-top: -0.5rem;
            margin-bottom: 1.5rem;
        }

        /* Chat messages */
        [data-testid="stChatMessage"] {
            background-color: #FFFFFF;
            color: #1F2937;
            border: 1px solid #D1D5DB;
            border-radius: 12px;
            padding: 0.75rem;
        }

        [data-testid="stChatMessage"] p,
        [data-testid="stChatMessage"] li,
        [data-testid="stChatMessage"] strong,
        [data-testid="stChatMessage"] span {
            color: #1F2937 !important;
        }

        /* Chat input */
        [data-testid="stChatInput"] textarea {
            color: #111827 !important;
            background-color: #FFFFFF !important;
            -webkit-text-fill-color: #111827 !important;
            caret-color: #111827 !important;
        }

        [data-testid="stChatInput"] textarea::placeholder {
            color: #6B7280 !important;
            -webkit-text-fill-color: #6B7280 !important;
            opacity: 1;
        }

        [data-testid="stChatInput"] {
            background-color: #FFFFFF;
            border-color: #D1D5DB;
        }

        /* Suggested question buttons */
        div.stButton > button {
            color: #1F2937 !important;
            background-color: #FFFFFF !important;
            border: 1px solid #D1D5DB;
            border-radius: 8px;
        }

        div.stButton > button:hover {
            color: #166534 !important;
            border-color: #39804D;
        }

        /* Source expanders */
        [data-testid="stExpander"] {
            background-color: #FFFFFF;
            border: 1px solid #D1D5DB;
            border-radius: 8px;
        }

        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] summary p {
            color: #1F2937 !important;
        }

        /* Secondary text */
        [data-testid="stCaptionContainer"] p {
            color: #4B5563 !important;
        }

        hr {
            border-color: #E5E7EB;
        }

        /* Make the bottom chat input area white */
        [data-testid="stBottom"] {
            background-color: #FFFFFF !important;
        }

        [data-testid="stBottom"] > div {
            background-color: #FFFFFF !important;
        }

        [data-testid="stChatInput"] {
            background-color: #FFFFFF !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 10px !important;
            box-shadow: none !important;
        }

        [data-testid="stChatInput"] > div {
            background-color: #FFFFFF !important;
        }

        [data-testid="stChatInput"] textarea {
            color: #1F2937 !important;
            background-color: #FFFFFF !important;
            -webkit-text-fill-color: #1F2937 !important;
            caret-color: #1F2937 !important;
        }

        [data-testid="stChatInput"] textarea::placeholder {
            color: #64748B !important;
            -webkit-text-fill-color: #64748B !important;
            opacity: 1 !important;
        }

        [data-testid="stChatInput"] button {
            color: #FFFFFF !important;
            background-color: #39804D !important;
            border-radius: 8px !important;
        }

        [data-testid="stChatInput"] button:hover {
            background-color: #28683A !important;
        }

    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# Header and existing logo
# --------------------------------------------------
if LOGO_PATH.exists():
    st.image(str(LOGO_PATH), width=150)

st.title("Amanara AI Chatbot")

st.markdown(

    """
    <p class="amanara-subtitle">
        Ask questions about Amanara's open-access solar power services.
    </p>

    """,
    unsafe_allow_html=True,
)

st.divider()

# --------------------------------------------------
# Initialize chatbot and conversation history
# --------------------------------------------------
if "chatbot" not in st.session_state:
    st.session_state.chatbot = AmanaraRAG()

if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------------------------------
# Display previous messages and their sources
# --------------------------------------------------
def display_sources(sources):
    if not sources:
        return

    with st.expander("Sources used"):
        for index, source in enumerate(sources, start=1):
            payload = source.payload or {}

            st.markdown(
                f"**Source {index}:** "
                f"{payload.get('source', 'Unknown')}"
            )
            st.caption(
                f"Chunk ID: {payload.get('chunk_id', 'Unknown')}"
            )
            st.write(
                payload.get("text", "No source text available.")
            )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant":
            display_sources(message.get("sources", []))

# --------------------------------------------------
# Suggested questions
# --------------------------------------------------
if not st.session_state.messages:
    st.markdown("**Try asking:**")

    suggestions = [
        "How does open-access solar work?",
        "Who is eligible for open access?",
        "What are the benefits of solar power?",
    ]

    columns = st.columns(len(suggestions))

    for index, suggestion in enumerate(suggestions):
        if columns[index].button(
            suggestion,
            key=f"suggestion_{index}",
            use_container_width=True,
        ):
            st.session_state.pending_question = suggestion
            st.rerun()

# --------------------------------------------------
# Process a new question
# --------------------------------------------------
question = st.chat_input("Ask a question about Amanara...")

# Support both the chat input and suggested questions.
if not question:
    question = st.session_state.pop("pending_question", None)

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Finding information and generating an answer..."):
            try:
                result = st.session_state.chatbot.ask(
                    question=question,
                    history=st.session_state.messages[:-1],
                )

                answer = result["answer"]
                sources = result.get("sources", [])

                st.markdown(answer)
                display_sources(sources)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                    }
                )

            except Exception:
                st.error(
                    "The chatbot could not generate a response. "
                    "Please try again."
                )

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.divider()

st.caption(
    "Amanara AI Chatbot | Student project prototype. "
    "Responses are based on the available knowledge base "
    "and should be verified before making business decisions."
)
