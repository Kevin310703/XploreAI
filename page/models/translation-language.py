import streamlit as st
import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("TRANSLATE_API")

# Kiểm tra nếu API_URL không tồn tại
if not API_URL:
    st.error("❌ Lỗi: API_URL chưa được cấu hình trong file .env")
    st.stop()

st.title("📝 AI Dịch Ngôn Ngữ - English to Vietnamese")

input_text = st.text_area("Nhập văn bản tiếng Anh cần dịch:", height=150)

if st.button("Dịch Ngay 🏆"):
    if input_text.strip():
        # Gửi request đến API
        payload = {"text": input_text}
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            translated_text = response.json().get("translated_text", "Lỗi không xác định")
            st.success("✅ Bản dịch:")
            st.write(f"**{translated_text}**")
        else:
            st.error("❌ Không thể dịch. Vui lòng kiểm tra API.")
    else:
        st.warning("⚠️ Vui lòng nhập văn bản cần dịch!")

# Footer
st.markdown("---")
st.markdown("🚀 **Ứng dụng sử dụng mô hình dịch AI - T5 finetuned en-vi**")

