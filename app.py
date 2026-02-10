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

        # Expanded marking logic
        feedback = []

        # Structure checks
        if "index" in assignment_text.lower() or "contents" in assignment_text.lower():
            feedback.append("✔ Index or table of contents found.")
        else:
            feedback.append("✘ Index or table of contents missing. Please include one for clarity.")

        if "page" in assignment_text.lower():
            feedback.append("✔ Page numbers referenced.")
        else:
            feedback.append("✘ Page numbers not referenced. Please add page numbers to your assignment.")

        # Learning outcome titles
        if "1.1" in assignment_text or "1.2" in assignment_text or "1.3" in assignment_text:
            feedback.append("✔ Learning outcome titles present.")
        else:
            feedback.append("✘ Learning outcome titles missing. Please use them as section headings.")

        # Assessment criteria checks
        if "Health and Safety at Work Act 1974" in assignment_text:
            feedback.append("✔ Reference to Health and Safety at Work Act 1974 found.")
        else:
            feedback.append("✘ Missing reference to Health and Safety at Work Act 1974.")

        if "risk assessment" in assignment_text:
            feedback.append("✔ Evidence of risk assessment found.")
        else:
            feedback.append("✘ No evidence of risk assessment found. Please include a completed risk assessment.")

        if "Electricity at Work Regulations" in assignment_text or "Computer Misuse Act" in assignment_text:
            feedback.append("✔ Additional legislation referenced.")
        else:
            feedback.append("✘ No reference to additional legislation (e.g., Electricity at Work Regulations, Computer Misuse Act).")

        # Sources of information
        if "hse" in assignment_text.lower() or "company handbook" in assignment_text.lower() or "intranet" in assignment_text.lower():
            feedback.append("✔ Sources of health and safety information identified.")
        else:
            feedback.append("✘ Sources of health and safety information not identified. Please include references such as the HSE website or company handbook.")

        # Evidence of procedure
        if "email" in assignment_text.lower() or "screenshot" in assignment_text.lower() or "report" in assignment_text.lower():
            feedback.append("✔ Practical evidence of following procedures included.")
        else:
            feedback.append("✘ No practical evidence found (e.g., email chains, screenshots, hazard reports). Please include these as supporting evidence.")

        # Positive language and encouragement
        feedback.append("Thank you for your submission. Please review the feedback above and address any missing elements for your next submission.")

        st.header("Feedback")
        for item in feedback:
            st.write(item)

    else:
        st.warning("PDF marking logic not yet implemented.")

st.info("This app is free to use. Upload an assignment and view the knowledge base above.")