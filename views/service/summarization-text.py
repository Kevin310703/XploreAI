import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
API_URL = os.getenv("SUMMARIZE_API")

if not API_URL:
    st.error("❌ Error: API_URL is not configured in the .env file.")
    st.stop()

st.title("📖 AI Text Summarization")

input_text = st.text_area("📝 Enter the text to summarize:", height=250)

if st.button("Summarize 📌"):
    if input_text.strip():
        st.info("⏳ Summarizing text, please wait...")

        # Send request to API
        payload = {"text": input_text}
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            summary = response.json().get("summary", "Unknown error")

            if summary:
                st.success("✅ Summary result:")
                st.write(f"**{summary}**")
            else:
                st.error("⚠️ API did not return a valid summary.")
        else:
            st.error("❌ Unable to summarize text. Please check the API.")
    else:
        st.warning("⚠️ Please enter text to summarize!")

st.markdown("---")
st.markdown("🚀 **This application uses the Pegasus-Samsum model for text summarization.**")
