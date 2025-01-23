import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

# Lấy API_URL từ file .env
API_URL = os.getenv("SUMMARIZE_API")

# Kiểm tra nếu API_URL chưa được cấu hình
if not API_URL:
    st.error("❌ Lỗi: API_URL chưa được cấu hình trong file .env")
    st.stop()

# Tiêu đề ứng dụng
st.title("📖 AI Tóm Tắt Văn Bản")

# Nhập văn bản từ người dùng
input_text = st.text_area("📝 Nhập văn bản cần tóm tắt:", height=250)

# Nút gửi yêu cầu tóm tắt
if st.button("Tóm Tắt 📌"):
    if input_text.strip():
        st.info("⏳ Đang tóm tắt văn bản, vui lòng chờ...")

        # Gửi request đến API
        payload = {"text": input_text}
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            summary = response.json().get("summary", "Lỗi không xác định")

            if summary:
                st.success("✅ Kết quả tóm tắt:")
                st.write(f"**{summary}**")
            else:
                st.error("⚠️ API không trả về nội dung tóm tắt hợp lệ.")
        else:
            st.error("❌ Không thể tóm tắt văn bản. Vui lòng kiểm tra API.")
    else:
        st.warning("⚠️ Vui lòng nhập văn bản cần tóm tắt!")

# Footer
st.markdown("---")
st.markdown("🚀 **Ứng dụng sử dụng mô hình Pegasus-Samsum để tóm tắt văn bản**")
