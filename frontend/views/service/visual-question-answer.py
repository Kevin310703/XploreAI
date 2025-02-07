import streamlit as st
import requests
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
API_URL = os.getenv("VQA_API")

if not API_URL:
    st.error("❌ Error: VQA API URL is not configured in the .env file.")
    st.stop()

st.title("🖼️ Visual Question Answering (VQA)")

uploaded_file = st.file_uploader("📤 Upload an image:", type=["png", "jpg", "jpeg"])
question = st.text_input("❓ Ask a question about the image:")

if uploaded_file and question:
    image = Image.open(uploaded_file)
    st.image(image, caption="📷 Uploaded Image", use_container_width =True)

    if st.button("🔍 Get Answer"):
        with st.spinner("⏳ Processing..."):
            files = {"image": uploaded_file.getvalue()}
            data = {"question": question}
            
            try:
                response = requests.post(API_URL, files=files, data=data, timeout=30)

                if response.status_code == 200:
                    answer = response.json().get("answer", "No answer received.")
                    st.success("✅ Answer:")
                    st.write(f"**{answer}**")
                else:
                    st.error(f"❌ API error: {response.status_code} - {response.text}")

            except requests.exceptions.Timeout:
                st.error("⏳ API request timed out. Please try again.")

            except requests.exceptions.RequestException as e:
                st.error(f"⚠️ API request failed: {e}")

st.markdown("---")
st.markdown("🚀 **This application uses the `VietKien/blip-vqa-finetuned` model for Visual Question Answering.**")
