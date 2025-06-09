import streamlit as st
from features.controllers.prompt_controller import PromptController

st.set_page_config(page_title="AI Crime Scene Investigator", layout="wide")
st.title("AI Crime Scene Investigator")

controller = PromptController()

uploaded_file = st.file_uploader("Upload a crime scene description (.txt)", type=["txt"])
if uploaded_file:
    description = uploaded_file.read().decode("utf-8")
    st.text_area("Crime Scene Text", value=description, height=200)

    if st.button("Analyze"):
        with st.spinner("Running AI analysis..."):
            result = controller.process_description(description)
            st.subheader("🔍 Analysis Result")
            st.write(result)