import streamlit as st
import requests
from config import API_BASE_URL_BACKEND_SERVICE

if not API_BASE_URL_BACKEND_SERVICE:
    raise ValueError("🚨 API base url is not set in the environment variables!")

# Component of page
with st.form("text_summarization_form", enter_to_submit =True, border=False):
    st.title("📖 Text Summarization")

    with st.expander("ℹ️ How to Use", expanded=False):
        st.markdown("""
            🔹 **Step 1:** Enter the text you want to summarize in the input box below.  
            🔹 **Step 2:** Click **"Summarize 📌"** to generate the summary.  
            🔹 **Step 3:** The summarized text will be displayed instantly.  
    
            ⚠️ **Note:**  
            - The model performs best on structured text with proper grammar.  
            - If you encounter errors, please check your input or ensure your connection or internet stability.  
        """)

    input_text = st.text_area("📝 Enter the text to summarize:", height=250, placeholder="Type or paste your text here...")

    submitted = st.form_submit_button("Summarize 📌")
    if submitted:
        with st.spinner("⏳ Processing..."):
            if input_text.strip():
                payload = {"text": input_text}
                
                try:
                    response = requests.post(f"{API_BASE_URL_BACKEND_SERVICE}/summarize", json=payload, timeout=120)

                    if response.status_code == 200:
                        summary = response.json().get("summary", "Unknown error")

                        if summary:
                            st.success("✅ Summary result:")
                            st.write(f"**{summary}**")
                        else:
                            st.error("⚠️ API did not return a valid summary.")
                    else:
                        st.error(f"❌ API error: {response.status_code}, Response: {response.text}")

                except requests.exceptions.Timeout:
                    st.error("⏳ API request timed out. Try again with a smaller text or check the server.")

                except requests.exceptions.ConnectionError:
                    st.error("⚠️ Could not connect to API. Is the server running?")

                except requests.exceptions.RequestException as e:
                    st.error(f"⚠️ API request failed: {e}")

            else:
                st.warning("⚠️ Please enter text to summarize!")

st.markdown("---")
st.markdown("🚀 **© 2025 X-OR AI GENERATIVE**")
