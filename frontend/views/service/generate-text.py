import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Loading env
load_dotenv()
API_URL = os.getenv("GENERATE_TEXT_API")

if not API_URL:
    st.error("❌ Error: API_URL is not configured in the .env file.")
    st.stop()

# Component of page
st.title("💬 Text Generation")

input_text = st.text_area("📝 Enter your text prompt:", height=150, placeholder="Write your input here...")

if st.button("Generate Text 🚀"):
    with st.spinner("⏳ Processing..."):
        if input_text.strip():
            payload = {"text": input_text}
            response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                generated_text = response.json().get("generated_text", "")
                st.success("✅ Generated Text:")
                st.write(f"**{generated_text}**")
            else:
                st.error(f"❌ API Error: {response.status_code}")
        else:
            st.warning("⚠️ Please enter text!")

st.markdown("---")
st.markdown("🚀 **Powered by OPT-2.7B LoRA fine-tuned model**")
