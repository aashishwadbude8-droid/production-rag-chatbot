import streamlit as st

from core.loader import load_pdfs
from core.chunker import create_chunks
from core.vectorstore import build_vectorstore
from core.retriever import build_bm25, hybrid_search
from core.answer_engine import answer_query
from core.llm_engine import ask_llm

# ------------------------------------
# PAGE CONFIGimport
# ------------------------------------

st.set_page_config(
    page_title="Production RAG",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Production RAG Assistant")
st.write("Ask questions from your PDFs")


# ------------------------------------
# SESSION STATE
# ------------------------------------

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "bm25" not in st.session_state:
    st.session_state.bm25 = None

if "chunks" not in st.session_state:
    st.session_state.chunks = []

if "documents" not in st.session_state:
    st.session_state.documents = []

if "messages" not in st.session_state:
    st.session_state.messages = []


# ------------------------------------
# PDF UPLOAD
# ------------------------------------

uploaded_files = st.file_uploader(
    "Upload PDF",
    type="pdf",
    accept_multiple_files=True
)


# ------------------------------------
# BUILD RAG
# ------------------------------------

if uploaded_files:

    with st.spinner("Processing PDFs..."):

        documents = load_pdfs(uploaded_files)

        chunks = create_chunks(documents)

        vectorstore = build_vectorstore(chunks)

        bm25 = build_bm25(chunks)

        st.session_state.documents = documents
        st.session_state.chunks = chunks
        st.session_state.vectorstore = vectorstore
        st.session_state.bm25 = bm25

    st.success("✅ Production RAG Ready!")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Pages", len(documents))

    with col2:
        st.metric("Chunks", len(chunks))


# ------------------------------------
# CHAT HISTORY
# ------------------------------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.write(msg["content"])


# ------------------------------------
# CHAT
# ------------------------------------

 

if query:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    with st.chat_message("user"):
        st.write(query)

    # -------------------------
    # Generate Answer
    # -------------------------

    if st.session_state.vectorstore is None:

        answer = "Please upload a PDF first."
        mode = "system"

    else:

        docs = hybrid_search(
            query,
            st.session_state.vectorstore,
            st.session_state.bm25
        )

        answer, mode = answer_query(
            query,
            docs
        )

        if mode == "pdf_context":

            context = "\n\n".join(
                doc.page_content
                for doc in docs
            )

            history = []

            for m in st.session_state.messages[-6:]:

                history.append(
                    {
                        "role": m["role"],
                        "content": m["content"]
                    }
                )

            answer = ask_llm(
                question=query,
                context=context,
                history=history
            )

            mode = "pdf + llm"

    # -------------------------
    # Assistant Response
    # -------------------------

query = st.chat_input("Ask your question...")

if query:

    # user message

    ...

    # answer generate

    ...

    import time

    with st.chat_message("assistant"):

        placeholder = st.empty()

        response = ""

        for word in answer.split():

            response += word + " "

            placeholder.markdown(response)

            time.sleep(0.03)

        st.caption(f"Mode : {mode}")

        if (
            st.session_state.vectorstore is not None
            and len(docs) > 0
        ):

            st.markdown("---")
            st.markdown("## 📄 Sources")

            shown = set()

            for doc in docs:

                filename = doc.metadata.get("filename", "Unknown")
                page = doc.metadata.get("page", 0) + 1

                key = (filename, page)

                if key in shown:
                    continue

                shown.add(key)

                with st.expander(f"📄 {filename} | Page {page}"):

                    st.write(doc.page_content[:500])

                    if len(doc.page_content) > 500:
                        st.write("...")

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )