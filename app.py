import streamlit as st
from docx import Document

st.title("BTEC Marking Agent – Unit 101: Health and Safety in ICT")

def load_knowledge(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

knowledge = load_knowledge("unit101_knowledge.txt")
st.header("Knowledge Base")
st.text_area("Unit 101 Knowledge", knowledge, height=300)

uploaded_file = st.file_uploader("Upload student assignment (Word or PDF)", type=["docx", "pdf"])
if uploaded_file:
    st.success("Assignment uploaded!")

    # Extract text from Word document
    if uploaded_file.name.endswith(".docx"):
        doc = Document(uploaded_file)
        assignment_text = "\n".join([para.text for para in doc.paragraphs])
        st.write("Assignment content preview:")
        st.text_area("Assignment Text", assignment_text, height=300)

        # Simple marking logic: check for key phrases
        feedback = []
        if "Health and Safety at Work Act 1974" in assignment_text:
            feedback.append("✔ Reference to Health and Safety at Work Act 1974 found.")
        else:
            feedback.append("✘ Missing reference to Health and Safety at Work Act 1974.")

        if "risk assessment" in assignment_text:
            feedback.append("✔ Evidence of risk assessment found.")
        else:
            feedback.append("✘ No evidence of risk assessment found.")

        if "learning outcome" in assignment_text or "1.1" in assignment_text:
            feedback.append("✔ Learning outcome titles present.")
        else:
            feedback.append("✘ Learning outcome titles missing.")

        st.header("Feedback")
        for item in feedback:
            st.write(item)

    else:
        st.warning("PDF marking logic not yet implemented.")

st.info("This app is free to use. Upload an assignment and view the knowledge base above.")