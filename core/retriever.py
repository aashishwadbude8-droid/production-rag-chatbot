from langchain_community.retrievers import BM25Retriever


def build_bm25(chunks, k=5):
    retriever = BM25Retriever.from_documents(chunks)
    retriever.k = k
    return retriever


def hybrid_search(query, vectorstore, bm25, top_k=5):

    # Dense Search with scores
    dense_results = vectorstore.similarity_search_with_score(
        query,
        k=top_k
    )

    dense_docs = []
    scores = []

    for doc, score in dense_results:
        dense_docs.append(doc)
        scores.append(score)

    # BM25 Search
    sparse_docs = bm25.invoke(query)

    merged = []
    seen = set()

    for doc in dense_docs + sparse_docs:

        key = (
            doc.metadata.get("filename", ""),
            doc.metadata.get("page", ""),
            doc.page_content
        )

        if key not in seen:
            seen.add(key)
            merged.append(doc)

    # -----------------------------
    # Confidence Score
    # -----------------------------

    if len(scores) == 0:
        confidence = 0

    else:

        best_score = min(scores)

        confidence = max(
            0,
            1 - best_score / 2
        )

    return merged[:top_k], confidence