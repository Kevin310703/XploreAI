import streamlit as st
import requests
from PIL import Image
from config import API_BASE_URL_BACKEND_SERVICE

if not API_BASE_URL_BACKEND_SERVICE:
    raise ValueError("🚨 API base url is not set in the environment variables!")

with st.form("vqa_form", enter_to_submit =True, border=False):
    st.title("🖼️ Visual Question Answering (VQA)")

    with st.expander("ℹ️ How to Use", expanded=False):
        st.markdown("""
            🔹 **Step 1:** Upload an image by clicking on **"📤 Upload an image"**.  
            🔹 **Step 2:** Type your question related to the image in the text area.  
            🔹 **Step 3:** Click **"Get Answer 🔍"** to process your question.  
            🔹 **Step 4:** The AI will analyze the image and provide an answer based on your question.  

            ⚠️ **Note:**  
            - Make sure to upload a clear image for better accuracy.  
            - Provide specific and clear questions to get the best responses.    
            - If the response takes too long, check your internet connection.  
        """)

    uploaded_file = st.file_uploader("📤 Upload an image:", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="📷 Uploaded Image", use_container_width =True)

    question = st.text_area("❓ Ask a question about the image:", height=150, placeholder="Enter your question")

    submitted = st.form_submit_button("Get Answer 🔍 ")
    if submitted:
        with st.spinner("⏳ Processing..."):
            files = {"image": uploaded_file.getvalue()}
            data = {"question": question}
            
            try:
                response = requests.post(f"{API_BASE_URL_BACKEND_SERVICE}/vqa/", files=files, data=data, timeout=30)

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
st.markdown("🚀 **© 2025 X-OR AI GENERATIVE**")
