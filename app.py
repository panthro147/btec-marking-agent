import streamlit as st
from docx import Document
import openai
import os

# --- Password Prompt (always appears) ---
password = st.text_input("Enter password to access the marking agent:", type="password")
if password != "Roxieandcleothecats1!":
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
Review the student's assignment below against the following criteria:

{knowledge}

Assignment:
{assignment_text}

Instructions:
- For each learning outcome, say if it’s fully met, partly met, or not met.
- Give one positive comment and one suggestion for improvement per outcome.
- Keep feedback under 500 words.
- Use UK English throughout.
- Use a friendly, supportive tone—imagine you’re chatting with the student and want them to feel confident and motivated.
- Avoid formal or academic language; be clear, encouraging, and down-to-earth.
- Use phrases like "Well done", "Great effort", "Keep going", "You’re nearly there", "Try adding...", "Next time, you could..."
- Don’t rewrite the assignment.
- If the assignment is incomplete, review only what’s present.
- End with a brief summary saying if the assignment is good enough to pass, and encourage the student to keep improving.
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