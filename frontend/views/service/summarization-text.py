import streamlit as st
import requests
from config import API_BASE_URL_CONTAINER

if not API_BASE_URL_CONTAINER:
    raise ValueError("🚨 API base url is not set in the environment variables!")

# Component of page
st.title("📖 Text Summarization")

input_text = st.text_area("📝 Enter the text to summarize:", height=250)

if st.button("Summarize 📌"):
    with st.spinner("⏳ Processing..."):
        if input_text.strip():
            payload = {"text": input_text}
            
            try:
                response = requests.post(f"{API_BASE_URL_CONTAINER}/summarize", json=payload, timeout=120)

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
st.markdown("🚀 **This application uses the Pegasus-Samsum model for text summarization.**")
