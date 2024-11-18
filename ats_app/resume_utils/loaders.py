"""
Author: Ayush Agarwal
"""
from langchain_community.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader


def load_resume_from_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    doc = loader.load()
    resume_text = ""
    for page in doc:
        resume_text+= page.page_content
    return resume_text

def load_resume_from_docx(docx_path):
    loader = UnstructuredWordDocumentLoader(docx_path)
    doc = loader.load()
    resume_text = ""
    for page in doc:
        resume_text+= page.page_content
    return resume_text
