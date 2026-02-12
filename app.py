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
Only use the content of the knowledge file below for all grading, definitions, and feedback. Do not use the internet, external sources, or your own assumptions.

{knowledge}

Assignment:
{assignment_text}

Instructions:
- For each criterion, clearly mark the status using symbols AFTER the criterion, e.g.:
    LO1 – P1: 🟢 Fully met
    LO1 – M1: 🟡 Partly met
    LO2 – P3: 🔴 Not met
    LO3 – M2: ⚪ Not applicable
- Review and provide feedback only for criteria present in BOTH the knowledge file and the assignment.
- Do not mention criteria missing from the knowledge file.
- For each learning outcome, give ONE short positive comment and ONE short suggestion (one sentence each).
- If a criterion is mostly met with minor omissions, treat it as met, but mention how to strengthen it.
- If work is borderline between grades, state that explicitly.
- Indicate which grade (Pass, Merit, or Distinction) is currently achievable.
- If criteria are incomplete, say what is needed for the next grade.
- If the assignment is partial, only assess what is present.
- Check for possible plagiarism or unreferenced AI-generated writing (tone shifts, repeated phrasing, inconsistent style). Flag if suspected.
- Do not rewrite or summarise the assignment.
- Keep all feedback under 400 words.
- Use UK English.
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