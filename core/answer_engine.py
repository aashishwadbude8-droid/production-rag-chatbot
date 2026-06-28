import re

from core.extractor import extract_variables


def answer_query(query, docs):
    """
    Main answer engine.

    Returns:
        answer
        mode
    """

    query_lower = query.lower()

    # -----------------------------
    # Extract variables from docs
    # -----------------------------
    variables = extract_variables(docs)

    # -----------------------------
    # Value Question
    # -----------------------------
    m = re.search(r"value of ([a-zA-Z_]\w*)", query_lower)

    if not m:
        m = re.search(r"([a-zA-Z_]\w*) ka value", query_lower)

    if m:

        var = m.group(1)

        if var in variables:

            return (
                variables[var]["value"],
                "pdf_variable"
            )

    # -----------------------------
    # Datatype Question
    # -----------------------------
    if "datatype" in query_lower or "type" in query_lower:

        m = re.search(r"([a-zA-Z_]\w*)", query_lower)

        if m:

            var = m.group(1)

            if var in variables:

                return (
                    variables[var]["datatype"],
                    "pdf_variable"
                )

    # -----------------------------
    # PDF Context Search
    # -----------------------------
    context = ""

    for doc in docs:

        context += doc.page_content + "\n"

    return (
        context[:1200],
        "pdf_context"
    )