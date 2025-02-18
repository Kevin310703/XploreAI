import streamlit as st
import requests
from config import API_BASE_URL_BACKEND_SERVICE

if not API_BASE_URL_BACKEND_SERVICE:
    raise ValueError("🚨 API base url is not set in the environment variables!")

# Component of page
with st.form("language_translation_form", enter_to_submit =True, border=False):
    st.title("📝 En-Vi Language Translation")

    with st.expander("ℹ️ How to Use", expanded=False):
        st.markdown("""
            🔹 **Step 1:** Select the translation direction using the dropdown menu.  
            🔹 **Step 2:** Enter the text you want to translate in the text box below.  
            🔹 **Step 3:** Click **"Translate Now 🏆"** to process the translation.  
            🔹 **Step 4:** The translated text will appear below.  

            ⚠️ **Note:**  
            - The AI model supports translation between **English and Vietnamese**.  
            - Use clear and grammatically correct sentences for better translation accuracy.  
            - If the translation does not work, check your connection or internet stability.  
        """)

    translation_direction = st.selectbox("Select Translation Direction:", 
                                        ["English → Vietnamese", "Vietnamese → English"])

    placeholder_text = ("Translate English text to translate to Vietnamese..." if translation_direction == "English → Vietnamese"
                        else "Nhập văn bản tiếng Việt để dịch sang tiếng Anh...")

    input_text = st.text_area("Enter your text:", height=200, placeholder=placeholder_text)

    submitted = st.form_submit_button("Translate Now 🏆")
    if submitted:
        with st.spinner("⏳ Processing..."):
            if input_text.strip():
                if translation_direction == "English → Vietnamese":
                    payload = {"text": f"en: {input_text}"}
                else:
                    payload = {"text": f"vi: {input_text}"}
                    
                response = requests.post(f"{API_BASE_URL_BACKEND_SERVICE}/translate", json=payload)

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
st.markdown("🚀 **© 2025 X-OR AI GENERATIVE**")
