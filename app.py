import streamlit as st
from docx import Document
from pptx import Presentation
import openai
import os

# --- Custom CSS for lusion.co-inspired style and larger drop area ---
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #1a2a6c 0%, #b21f1f 50%, #fdbb2d 100%);
}
.big-container {
    padding: 40px 0 0 0;
    border-radius: 24px;
    background: rgba(255,255,255,0.85);
    box-shadow: 0 8px 32px 0 rgba(31,38,135,0.37);
    margin-bottom: 32px;
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
}
.upload-label {
    font-size: 2.2rem;
    font-weight: bold;
    color: #1a2a6c;
    margin-bottom: 16px;
    text-align: center;
    letter-spacing: 1px;
}
.lusion-drop-area {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 220px;
    border: 3px dashed #4F8BF9;
    border-radius: 20px;
    background: #F0F6FF;
    margin-bottom: 24px;
    margin-top: 8px;
}
.feedback-container {
    padding: 32px;
    border-radius: 16px;
    background: #fff;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    margin-top: 32px;
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
}
</style>
""", unsafe_allow_html=True)

# --- Password Prompt (always appears) ---
password = st.text_input("Enter password to access the marking agent:", type="password")
if password != "Roxieandcleothecats1!":
    st.warning("Please enter the correct password to continue.")
    st.stop()

st.markdown("<div class='big-container'>", unsafe_allow_html=True)
st.title("OCR and BTEC Marking Agent (AI-Powered)")
st.markdown("</div>", unsafe_allow_html=True)

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

st.markdown("<div class='big-container'>", unsafe_allow_html=True)
st.header(f"Knowledge Base for {selected_unit}")
st.text_area("Knowledge", knowledge, height=300)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='big-container'><div class='upload-label'>Upload Your Assignment Files</div>", unsafe_allow_html=True)
st.markdown("<div class='lusion-drop-area'>", unsafe_allow_html=True)
uploaded_files = st.file_uploader(
    "",
    type=["docx", "pptx"],
    accept_multiple_files=True,
    key="lusion_drop"
)
st.markdown("</div></div>", unsafe_allow_html=True)

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
    st.markdown("<div class='feedback-container'><h3>Assignment Content Preview</h3>", unsafe_allow_html=True)
    st.text_area("Assignment Text", assignment_text, height=300)
    st.markdown("</div>", unsafe_allow_html=True)
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
- If the knowledge file does not contain Merit or Distinction criteria for a learning outcome or assessment point, do not grade or comment on those criteria.
- For each criterion, state if it is fully met, partly met, or not met, and use a traffic light symbol: 🟢 for fully met, 🟡 for partly met, and 🔴 for not met.
- For criteria that are not met, provide a concise explanation of what is missing and a clear, actionable suggestion for improvement (3–4 sentences).
- For criteria that are partly met, briefly state what is covered, what is missing, and how the student can fully meet the criterion (3–4 sentences).
- If a criterion is mostly met and only minor detail is missing, consider it as met for grading purposes, but mention what could be improved for a stronger grade.
- If the work is borderline between two grades, state this in your summary and explain your reasoning.
- For each learning outcome, give one short positive comment and one short suggestion for improvement (each no more than one sentence).
- Indicate which grading level is currently achievable: Pass, Merit, or Distinction.
- If some criteria are missing or incomplete, briefly advise what is needed for the next grade.
- If the assignment is incomplete or a partial submission, review only what is present and give brief guidance for improvement.
- If you suspect any content is AI-generated and not referenced, flag this and remind the student that unreferenced AI-generated work is not allowed.
- Do not rewrite or summarise the assignment; only review and comment.
- Keep the entire feedback under 1000 tokens.
- Use UK English throughout.
- Use a friendly, supportive, and motivating tone. Avoid formal or academic language.
- Do not include a greeting or sign-off.
- End with a brief summary (max two sentences) stating what grade is currently achievable and encourage the student to keep improving.
"""
            try:
                response = openai.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=[{"role": "user", "content": improved_prompt}],
                    max_tokens=1000,
                    temperature=0.2,
                )
                feedback = response.choices[0].message.content
                st.markdown("<div class='feedback-container'><h3>AI-Powered Feedback</h3>", unsafe_allow_html=True)
                st.write(feedback)
                st.markdown("</div>", unsafe_allow_html=True)
            except openai.RateLimitError:
                st.error("OpenAI rate limit reached. Please wait and try again later, or check your usage at https://platform.openai.com/usage.")

st.info("This app is free to use. Select your unit, upload up to two assignment files, and view the knowledge base above.")