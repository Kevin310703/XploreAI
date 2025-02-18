import streamlit as st
import requests
from config import API_BASE_URL_BACKEND_SERVICE

if not API_BASE_URL_BACKEND_SERVICE:
    raise ValueError("🚨 API base url is not set in the environment variables!")

# Component of page
with st.form("text_generator_form", enter_to_submit =True, border=False):
    st.title("💬 Text Generation")
    with st.expander("ℹ️ How to Use", expanded=False):
        st.markdown("""
            🔹 **Step 1:** Enter a text prompt in the input box below.  
            🔹 **Step 2:** Click **"Generate Text 🚀"** to generate the response.  
            🔹 **Step 3:** The generated text will be displayed instantly.  
    
            ⚠️ **Note:**  
            - The model performs best on well-structured prompts.  
            - If the response takes too long, try reducing the input length.  
            - Ensure you are logged in and your connection or internet stability.  
        """)

    input_text = st.text_area("📝 Enter your text prompt:", height=150, placeholder="Write your input here...")

    submitted = st.form_submit_button("Generate Text 🚀")
    if submitted:
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
st.markdown("🚀 **© 2025 X-OR AI GENERATIVE**")
