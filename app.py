import streamlit as st
from docx import Document
from pptx import Presentation
import openai
import os

# --- Password Prompt ---
password = st.text_input("Enter password to access the marking agent:", type="password")
if password != "Roxieandcleothecats1!":
    st.warning("Please enter the correct password to continue.")
    st.stop()

st.title("OCR and BTEC Marking Agent (AI-Powered)")

openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

units = {
    "Unit 101 – Health and Safety in ICT": "unit101_knowledge.txt",
    "Unit 318 – Software Installation and Upgrade": "unit318_knowledge.txt",
    "Unit 22 – Big Data Analytics (OCR)": "unit22_knowledge.txt"
}

selected_unit = st.selectbox("Select unit to mark:", list(units.keys()))

def load_knowledge(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

knowledge = load_knowledge(units[selected_unit])

st.header(f"Knowledge Base for {selected_unit}")
st.text_area("Knowledge", knowledge, height=300)

uploaded_files = st.file_uploader(
    "Upload up to two files for the assignment (Word and/or PowerPoint)",
    type=["docx", "pptx"],
    accept_multiple_files=True
)

assignment_text = ""

if uploaded_files:
    st.success("Files uploaded!")
    slide_number = 1

    for uploaded_file in uploaded_files:
        if uploaded_file.name.endswith(".docx"):
            doc = Document(uploaded_file)
            assignment_text += "\n".join([para.text for para in doc.paragraphs]) + "\n"

        elif uploaded_file.name.endswith(".pptx"):
            prs = Presentation(uploaded_file)
            for slide in prs.slides:
                assignment_text += f"\n--- Slide {slide_number} ---\n"
                for shape in slide.shapes:
                    if hasattr(shape, "text") and shape.text.strip():
                        assignment_text += shape.text + "\n"
                slide_number += 1

    st.write("Combined assignment content preview:")
    st.text_area("Assignment Text", assignment_text, height=300)

    if st.button("Mark with AI"):
        with st.spinner("Marking…"):

            improved_prompt = f"""
You are an experienced OCR and BTEC assessor for {selected_unit} (Level 3).
Only use the content of the knowledge file below for all grading, definitions, and feedback. Do not use the internet or outside sources.

{knowledge}

Assignment:
{assignment_text}

Instructions:
- Review ALL criteria listed in the knowledge file.
- For each criterion, decide if the assignment shows:
    🟢 Fully met
    🟡 Partly met
    🔴 Not met
    ⚪ Not applicable (ONLY if the criterion does not exist in this unit at all)
  Place the symbol AFTER the criterion name, e.g.:
  LO1 – P1: 🟢 Fully met — Explanation…
- If evidence for a criterion is missing, mark it as 🔴 Not met (NOT "Not applicable").
- If a criterion is mostly met but missing small detail, treat it as met but mention how to improve.
- If the work is borderline between two grades, state this clearly.
- Provide ONE short positive comment and ONE short improvement suggestion per learning outcome.
- Indicate the grade currently achievable (Pass, Merit, Distinction).
- If assignment is incomplete, assess only what is present.
- Perform a basic similarity/plagiarism check based on sudden tone shifts, repeated structures, or inconsistent writing.
- Do not rewrite the assignment.
- Keep feedback under 400 words.
- No greeting or sign‑off.
- End with a brief two‑sentence summary and encouragement.
"""

            try:
                response = openai.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[{"role": "user", "content": improved_prompt}],
                    max_tokens=700,
                    temperature=0.2,
                )
                feedback = response.choices[0].message.content

                st.header("AI-Powered Feedback")
                st.write(feedback)

            except openai.RateLimitError:
                st.error("OpenAI rate limit reached. Please wait and try again later.")

st.info("This app is free to use. Select your unit, upload up to two assignment files, and view the knowledge base above.")