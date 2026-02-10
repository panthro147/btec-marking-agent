import streamlit as st
from docx import Document
import openai
import os

st.title("BTEC Marking Agent – Unit 101: Health and Safety in ICT (AI-Powered)")

# Securely load your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

def load_knowledge(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

knowledge = load_knowledge("unit101_knowledge.txt")
st.header("Knowledge Base")
st.text_area("Unit 101 Knowledge", knowledge, height=300)

uploaded_file = st.file_uploader("Upload student assignment (Word only for demo)", type=["docx"])
if uploaded_file:
    st.success("Assignment uploaded!")

    # Extract text from Word document
    doc = Document(uploaded_file)
    assignment_text = "\n".join([para.text for para in doc.paragraphs])
    st.write("Assignment content preview:")
    st.text_area("Assignment Text", assignment_text, height=300)

    # AI marking logic
    if st.button("Mark with AI"):
        with st.spinner("Marking..."):
            prompt = f"""
You are an experienced BTEC assessor for Unit 101 – Health and Safety in ICT (Level 3 NVQ).
Your marking must be based strictly on the following knowledge and assessment criteria:

{knowledge}

Here is the student's assignment:

{assignment_text}

Instructions:
- Review the assignment against the criteria above.
- Highlight what is done well.
- Clearly and positively point out any missing or incorrect elements.
- Keep feedback simple, positive, and in UK English.
- Do not rewrite the assignment.
- If the assignment is incomplete, review only what is present.

Provide your feedback below:
"""
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=600,
                temperature=0.2,
            )
            feedback = response.choices[0].message.content
            st.header("AI-Powered Feedback")
            st.write(feedback)

st.info("This app is free to use. Upload an assignment and view the knowledge base above.")