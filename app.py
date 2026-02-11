import streamlit as st

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    password = st.text_input("Enter password to access the marking agent:", type="password")
    if password == "Roxieandcleothecats1!":
        st.session_state["authenticated"] = True
        st.success("Password accepted. Please refresh the page to continue.")
        st.stop()
    elif password:
        st.warning("Please enter the correct password to continue.")
        st.stop()

st.title("You are past the password prompt!")