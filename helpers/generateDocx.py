from io import BytesIO
from docx import Document

def generate_docx(text):
    """Generate a DOCX file from text and return it as a BytesIO stream."""
    doc = Document()
    doc.add_paragraph(text)
    
    file_stream = BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)  # Reset pointer to the beginning
    return file_stream
