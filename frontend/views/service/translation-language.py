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

# 📌 Thêm phần hướng dẫn sử dụng
with st.expander("ℹ️ Hướng dẫn sử dụng", expanded=False):
    st.markdown("""
        🔹 **Bước 1:** Nhập đoạn văn bản tiếng Anh vào ô bên dưới.  
        🔹 **Bước 2:** Nhấn nút **"Translate Now 🏆"** để bắt đầu dịch.  
        🔹 **Bước 3:** Văn bản dịch sang tiếng Việt sẽ hiển thị ngay lập tức.  

        ⚠️ **Lưu ý:**  
        - Hệ thống hỗ trợ dịch văn bản chuẩn và có dấu câu đầy đủ để có kết quả tốt nhất.  
        - Nếu gặp lỗi, vui lòng kiểm tra lại API hoặc đảm bảo kết nối mạng ổn định.  
    """)
    
input_text = st.text_area("Enter the English text to translate:", height=150, placeholder="Translation from English to Vietnamese: ...")

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
