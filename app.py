import streamlit as st
from docx import Document
from pptx import Presentation
import openai
import os

# --- Password Prompt (always appears) ---
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
        with st.spinner("Marking..."):

            improved_prompt = f"""
You are an experienced OCR and BTEC assessor for {selected_unit} (Level 3).
Only use the content of the knowledge file below for all grading, definitions, and feedback. Do not use the internet, external sources, or your own assumptions.

{knowledge}

Assignment:
{assignment_text}

Instructions:
- Review and provide feedback only for criteria that are present in both the knowledge file and the assignment. Do not mention or grade criteria that are not present.
- For each learning outcome and assessment point, review the work against the Pass, Merit, and Distinction criteria in the knowledge file.
- If the knowledge file does not contain Merit or Distinction criteria, do not grade or comment on those criteria.
- For each criterion, state if it is fully met, partly met, or not met.
- If a criterion is mostly met and only minor detail is missing, consider it as met for grading purposes, but mention what could be improved for a stronger grade.
- If the work is borderline between two grades, state this in your summary and explain your reasoning.
- For each learning outcome, give one short positive comment and one short suggestion for improvement (each no more than one sentence).
- If some criteria are missing or incomplete, briefly advise what is needed for the next grade.
- Indicate which grading level is currently achievable: Pass, Merit, or Distinction.
- If the assignment is incomplete or a partial submission, review only what is present.
- Perform a basic similarity/plagiarism check by looking for repeated sentence structures, inconsistent writing style, overly formal tone, or sudden changes in complexity. If you suspect non‑original work or unreferenced AI‑generated content, flag this clearly.
- Do not rewrite or summarise the assignment; only review and comment.
- Keep the entire feedback under 400 words.
- Use UK English throughout.
- Use a friendly, supportive, motivating tone. Avoid formal or academic language.
- Do not include a greeting or sign-off.
- End with a brief summary (max two sentences) stating what grade is currently achievable and encourage the student to keep improving.
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

                # --- Marking Rubric Visual ---
                st.subheader("Marking Rubric Overview")

                criteria_status = {
                    "Fully met": "🟢",
                    "Partly met": "🟡",
                    "Not met": "🔴",
                    "Not applicable": "⚪"
                }

                st.write("Below is a visual summary of how each criterion was evaluated:")

                for line in feedback.split("\n"):
                    line_lower = line.lower()
                    if "fully met" in line_lower:
                        st.write(f"{criteria_status['Fully met']} {line}")
                    elif "partly met" in line_lower:
                        st.write(f"{criteria_status['Partly met']} {line}")
                    elif "not met" in line_lower:
                        st.write(f"{criteria_status['Not met']} {line}")
                    elif "not applicable" in line_lower:
                        st.write(f"{criteria_status['Not applicable']} {line}")

            except openai.RateLimitError:
                st.error("OpenAI rate limit reached. Please wait and try again later.")

st.info("This app is free to use. Select your unit, upload up to two assignment files, and view the knowledge base above.")