import streamlit as st
import requests
from config import API_BASE_URL_BACKEND_SERVICE

if not API_BASE_URL_BACKEND_SERVICE:
    raise ValueError("🚨 API base url is not set in the environment variables!")

# Component of page
st.title("💬 Text Generation")

input_text = st.text_area("📝 Enter your text prompt:", height=150, placeholder="Write your input here...")

if st.button("Generate Text 🚀"):
    with st.spinner("⏳ Processing..."):
        if input_text.strip():
            payload = {"text": input_text}

            try:
                response = requests.post(f"{API_BASE_URL_BACKEND_SERVICE}/generate-text", json=payload, timeout=60)

                if response.status_code == 200:
                    generated_text = response.json().get("generated_text", "")
                    st.success("✅ Generated Text:")
                    st.write(f"**{generated_text}**")
                else:
                    st.error(f"❌ API Error: {response.status_code}")

            except requests.exceptions.ReadTimeout:
                st.error("⏳ API took too long to respond. Try again with a shorter input.")

            except requests.exceptions.ConnectionError:
                st.error("🔌 Failed to connect to the API. Check your network or API status.")

        else:
            st.warning("⚠️ Please enter text!")

st.markdown("---")
st.markdown("🚀 **Powered by OPT-2.7B LoRA fine-tuned model**")
