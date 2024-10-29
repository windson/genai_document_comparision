import os
import PyPDF2
from config import *


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(file):
    if file and allowed_file(file.name):
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        file_path = os.path.join(UPLOAD_FOLDER, file.name)
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        return file_path
    return None


def read_pdf(file_path):
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        content = []

        for i in range(num_pages):
            page_content = pdf_reader.pages[i].extract_text()
            content.append(f"Page {i+1}:\n{page_content}")

        return "\n\n".join(content)


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
