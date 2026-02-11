import streamlit as st
from docx import Document
import openai
import os

# --- Password Prompt with session state ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    password = st.text_input("Enter password to access the marking agent:", type="password")
    if password == "Roxieandcleothecats1!":
        st.session_state["authenticated"] = True
    elif password:
        st.warning("Please enter the correct password to continue.")
    st.stop()
# -----------------------

st.title("BTEC Marking Agent (AI-Powered)")

openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

# Define available units and their knowledge files
units = {
    "Unit 101 – Health and Safety in ICT": "unit101_knowledge.txt",
    "Unit 318 – Software Installation and Upgrade": "unit318_knowledge.txt",
    # Add more units here as needed
}

selected_unit = st.selectbox("Select unit to mark:", list(units.keys()))

def load_knowledge(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

knowledge = load_knowledge(units[selected_unit])
st.header(f"Knowledge Base for {selected_unit}")
st.text_area("Knowledge", knowledge, height=300)

uploaded_file = st.file_uploader("Upload student assignment (Word only for demo)", type=["docx"])
if uploaded_file:
    st.success("Assignment uploaded!")

    doc = Document(uploaded_file)
    assignment_text = "\n".join([para.text for para in doc.paragraphs])
    st.write("Assignment content preview:")
    st.text_area("Assignment Text", assignment_text, height=300)

    if st.button("Mark with AI"):
        with st.spinner("Marking..."):
            improved_prompt = f"""
You are an experienced BTEC assessor for {selected_unit} (Level 3 NVQ).
Your marking must be based strictly on the following knowledge and assessment criteria:

{knowledge}

Here is the student's assignment:

{assignment_text}

Instructions:
- For each learning outcome, state whether it is:
  - Fully met
  - Partially met
  - Not met
- For each outcome, provide a brief reason for your judgement.
- Highlight what the student has done well, using positive and encouraging language.
- Clearly and simply point out any missing or incorrect elements, so the student knows what to improve for their next submission.
- If the assignment is incomplete, review only what is present.
- Do not rewrite the assignment.
- Use UK English throughout.

After reviewing all learning outcomes, provide a final summary stating whether the assignment is sufficient to pass according to the criteria, or if further work is needed. Be clear and positive in your language.
"""
            try:
                response = openai.chat.completions.create(
                    model="gpt-4.1-mini",  # Updated model name
                    messages=[{"role": "user", "content": improved_prompt}],
                    max_tokens=800,  # Output length limited to 800 tokens
                    temperature=0.2,
                )
                feedback = response.choices[0].message.content
                st.header("AI-Powered Feedback")
                st.write(feedback)
            except openai.RateLimitError:
                st.error("OpenAI rate limit reached. Please wait and try again later, or check your usage at https://platform.openai.com/usage.")

st.info("This app is free to use. Select your unit, upload an assignment, and view the knowledge base above.")