import streamlit as st

st.title("BTEC Marking Agent – Unit 101: Health and Safety in ICT")

# Load the knowledge file
def load_knowledge(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

knowledge = load_knowledge("unit101_knowledge.txt")

st.header("Knowledge Base")
st.text_area("Unit 101 Knowledge", knowledge, height=300)

# Assignment upload
uploaded_file = st.file_uploader("Upload student assignment (Word or PDF)", type=["docx", "pdf"])
if uploaded_file:
    st.success("Assignment uploaded! (Demo: marking logic would go here)")
    st.write("Feedback will appear here after marking.")

st.info("This app is free to use. Upload an assignment and view the knowledge base above.")