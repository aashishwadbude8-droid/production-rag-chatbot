import time
import streamlit as st

from core.loader import load_pdfs
from core.chunker import create_chunks
from core.vectorstore import build_vectorstore
from core.retriever import build_bm25, hybrid_search
from core.answer_engine import answer_query
from core.llm_engine import ask_llm, normal_chat


# -----------------------------------------
# PAGE CONFIG
# -----------------------------------------

st.set_page_config(
    page_title="Production RAG Assistant",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Production RAG Assistant")
st.caption("Production Ready RAG Chatbot")


# -----------------------------------------
# SESSION STATE
# -----------------------------------------

defaults = {
    "vectorstore": None,
    "bm25": None,
    "documents": [],
    "chunks": [],
    "messages": [],
}

for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value


# -----------------------------------------
# SIDEBAR
# -----------------------------------------

with st.sidebar:

    st.header("📂 Upload PDFs")

    uploaded_files = st.file_uploader(
        "Choose PDF Files",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:

        with st.spinner("Building Vector Database..."):

            documents = load_pdfs(uploaded_files)

            chunks = create_chunks(documents)

            vectorstore = build_vectorstore(chunks)

            bm25 = build_bm25(chunks)

            st.session_state.documents = documents
            st.session_state.chunks = chunks
            st.session_state.vectorstore = vectorstore
            st.session_state.bm25 = bm25

        st.success("✅ PDFs Indexed Successfully")

        st.metric("Pages", len(documents))
        st.metric("Chunks", len(chunks))

    st.divider()

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

        st.rerun()


# -----------------------------------------
# CHAT HISTORY
# -----------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# -----------------------------------------
# USER INPUT
# -----------------------------------------

query = st.chat_input("Ask anything...")

if query:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    with st.chat_message("user"):
        st.markdown(query)

    history = []

    for msg in st.session_state.messages[-6:]:

        history.append(
            {
                "role": msg["role"],
                "content": msg["content"]
            }
        )

    # -----------------------------------------
    # RETRIEVE DOCUMENTS
    # -----------------------------------------

    docs, confidence = hybrid_search(
        query,
        st.session_state.vectorstore,
        st.session_state.bm25
    )

    answer, mode = answer_query(
        query,
        docs
    )

    # -----------------------------------------
    # SMART ROUTING
    # -----------------------------------------

    if mode == "pdf_variable":

        pass

    elif mode == "pdf_context":

        context = "\n\n".join(
            doc.page_content
            for doc in docs
        )

        answer = ask_llm(
            question=query,
            context=context,
            history=history
        )

        mode = "pdf + llm"

    else:

        answer = normal_chat(
            question=query,
            history=history
        )

        mode = "general_chat"

    # -----------------------------------------
    # ASSISTANT RESPONSE
    # -----------------------------------------

    with st.chat_message("assistant"):

        placeholder = st.empty()

        response = ""

        for word in answer.split():

            response += word + " "

            placeholder.markdown(response)

            time.sleep(0.02)

        st.caption(f"Mode : {mode}")

        if len(docs) > 0:

            st.markdown("---")
            st.markdown("## 📄 Sources")

            shown = set()

            for doc in docs:

                filename = doc.metadata.get(
                    "filename",
                    "Unknown"
                )

                page = doc.metadata.get(
                    "page",
                    0
                ) + 1

                key = (filename, page)

                if key in shown:
                    continue

                shown.add(key)

                with st.expander(
                    f"📄 {filename} | Page {page}"
                ):

                    st.write(doc.page_content[:500])

                    if len(doc.page_content) > 500:
                        st.write("...")

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )