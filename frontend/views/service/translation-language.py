import streamlit as st
import os
import requests
from dotenv import load_dotenv

# Loading env
load_dotenv()
API_URL = os.getenv("TRANSLATE_API")

if not API_URL:
    st.error("❌ Error: API_URL is not configured in the .env file.")
    st.stop()

# Component of page
st.title("📝 AI Language Translation")

with st.expander("ℹ️ How to Use", expanded=False):
    st.markdown("""
        🔹 **Step 1:** Choose the translation direction (English → Vietnamese or Vietnamese → English).  
        🔹 **Step 2:** Enter the text in the input box below.  
        🔹 **Step 3:** Click **"Translate Now 🏆"** to start the translation.  
        🔹 **Step 4:** The translated text will be displayed instantly.  

        ⚠️ **Note:**  
        - The system provides the best results when translating well-formed sentences with correct punctuation.  
        - If you encounter errors, please check the API connection or ensure a stable internet connection.  
    """)

translation_direction = st.selectbox("Select Translation Direction:", 
                                     ["English → Vietnamese", "Vietnamese → English"])

placeholder_text = ("Translate English text to translate to Vietnamese..." if translation_direction == "English → Vietnamese"
                    else "Nhập văn bản tiếng Việt để dịch sang tiếng Anh...")

input_text = st.text_area("Enter your text:", height=200, placeholder=placeholder_text)

if st.button("Translate Now 🏆"):
    with st.spinner("⏳ Processing..."):
        if input_text.strip():
            language_pair = "en-vi" if translation_direction == "English → Vietnamese" else "vi-en"

            payload = {"text": input_text}
            response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                translated_text = response.json().get("translated_text", "Unknown error")
                st.success("✅ Translated Text:")
                st.write(f"**{translated_text}**")
            else:
                st.error("❌ Unable to translate. Please check the API.")
        else:
            st.warning("⚠️ Please enter text to translate!")

# Footer Section
st.markdown("---")
st.markdown("🚀 **This application uses an AI translation model.**")
