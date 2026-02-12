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
1. Review the assignment against the Pass, Merit, and Distinction criteria in the knowledge file.
2. If Merit or Distinction criteria are missing for any outcome, do not grade or comment on those criteria.
3. For each criterion, state if it is fully met, partly met, or not met.
4. Indicate which grading level is currently achievable: Pass, Merit, or Distinction.
5. Advise what additional work is needed to reach the next grade, if applicable.
6. If the assignment is incomplete or a partial submission, review only what is present and give guidance for improvement.
7. If you suspect any content is AI-generated and not referenced, flag this and remind the student that unreferenced AI-generated work is not allowed.
8. For each learning outcome, give one positive comment and one suggestion for improvement.
9. Do not rewrite or summarise the assignment; only review and comment.
10. Keep feedback under 500 words.
11. Use UK English throughout.
12. Use a friendly, supportive, and motivating tone. Avoid formal or academic language.
13. Use phrases like "Well done", "Great effort", "Keep going", "You’re nearly there", "Try adding...", "Next time, you could..."
14. End with a brief summary stating what grade is currently achievable and encourage the student to keep improving.
"""
            try:
                response = openai.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[{"role": "user", "content": improved_prompt}],
                    max_tokens=1000,  # Increased for more complete reviews
                    temperature=0.2,
                )
                feedback = response.choices[0].message.content
                st.header("AI-Powered Feedback")
                st.write(feedback)
            except openai.RateLimitError:
                st.error("OpenAI rate limit reached. Please wait and try again later, or check your usage at https://platform.openai.com/usage.")

st.info("This app is free to use. Select your unit, upload up to two assignment files, and view the knowledge base above.")