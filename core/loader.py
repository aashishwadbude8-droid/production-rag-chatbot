import fitz
from langchain_core.documents import Document


def load_pdfs(uploaded_files):
    documents = []

    for uploaded_file in uploaded_files:

        pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")

        for page_no, page in enumerate(pdf):

            text = page.get_text("text")

            if text.strip():

                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "filename": uploaded_file.name,
                            "page": page_no
                        }
                    )
                )

    return documents