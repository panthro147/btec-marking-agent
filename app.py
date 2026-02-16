import streamlit as st
from docx import Document
from pptx import Presentation
import PyPDF2
import openai
import os

# --- Password Prompt (always appears) ---
password = st.text_input("Enter password to access the marking agent:", type="password")
if password != "Roxieandcleothecats1!":
    st.warning("Please enter the correct password to continue.")
    st.stop()

st.title("OCR and BTEC Marking Agent (AI-Powered)")

openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

# Updated units dictionary with grading scheme
units = {
    "Unit 101 – Health and Safety in ICT": {"file": "unit101_knowledge.txt", "grading": "btec"},
    "Unit 318 – Software Installation and Upgrade": {"file": "unit318_knowledge.txt", "grading": "btec"},
    "Unit 22 – Big Data Analytics (OCR)": {"file": "unit22_knowledge.txt", "grading": "ocr"},
    "Unit 302 – Develop Own Effectiveness and Professionalism": {"file": "unit302_knowledge.txt", "grading": "btec"}
}

selected_unit = st.selectbox("Select unit to mark:", list(units.keys()))
unit_info = units[selected_unit]
knowledge = None

def load_knowledge(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

knowledge = load_knowledge(unit_info["file"])
grading_scheme = unit_info["grading"]

st.header(f"Knowledge Base for {selected_unit}")
st.text_area("Knowledge", knowledge, height=300)

# --- Clean, prominent uploader area ---
st.markdown("## Upload Your Assignment Files")
st.markdown(
    """
    Drag and drop up to two files (Word, PowerPoint, or PDF) below:
    """,
    unsafe_allow_html=True
)

uploaded_files = st.file_uploader(
    "",
    type=["docx", "pptx", "pdf"],
    accept_multiple_files=True,
    key="main_drop"
)

assignment_text = ""
if uploaded_files:
    st.success("Files uploaded!")
    for uploaded_file in uploaded_files:
        if uploaded_file.name.endswith(".docx"):
            doc = Document(uploaded_file)
            assignment_text += "\n".join([para.text for para in doc.paragraphs]) + "\n"
        elif uploaded_file.name.endswith(".pptx"):
            prs = Presentation(uploaded_file)
            for slide in prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        assignment_text += shape.text + "\n"
        elif uploaded_file.name.endswith(".pdf"):
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    assignment_text += page_text + "\n"

st.markdown("### Assignment Content Preview")
st.text_area("Assignment Text", assignment_text, height=300)

if st.button("Mark with AI"):
    with st.spinner("Marking..."):
        # Grading instructions based on scheme
        if grading_scheme == "btec":
            grading_instructions = """
- Only use Pass/Not Yet Achieved for grading. Do not mention Merit or Distinction.
- For each criterion, state if it is fully met (Pass) or not yet achieved, and use a traffic light symbol: 🟢 for fully met, 🔴 for not yet achieved.
- For criteria that are not yet achieved, provide a concise explanation of what is missing and a clear, actionable suggestion for improvement (1–2 sentences).
