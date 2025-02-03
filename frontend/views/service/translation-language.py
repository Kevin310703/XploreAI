import streamlit as st
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_URL = os.getenv("TRANSLATE_API")

if not API_URL:
    st.error("❌ Error: API_URL is not configured in the .env file.")
    st.stop()

st.title("📝 AI Language Translation - English to Vietnamese")

input_text = st.text_area("Enter the English text to translate:", height=150)

if st.button("Translate Now 🏆"):
    if input_text.strip():
        # Send request to API
        payload = {"text": input_text}
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            translated_text = response.json().get("translated_text", "Unknown error")
            st.success("✅ Translation:")
            st.write(f"**{translated_text}**")
        else:
            st.error("❌ Unable to translate. Please check the API.")
    else:
        st.warning("⚠️ Please enter text to translate!")

st.markdown("---")
st.markdown("🚀 **This application uses the AI translation model - T5 finetuned en-vi.**")
