import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

# Lấy API_URL từ file .env
API_URL = os.getenv("GENERATE_IMAGE_API")

# Kiểm tra nếu API_URL chưa được cấu hình
if not API_URL:
    st.error("❌ Lỗi: API_URL chưa được cấu hình trong file .env")
    st.stop()

# Tiêu đề ứng dụng
st.title("🎨 AI Tạo Hình Ảnh - Stable Diffusion")

# Nhập prompt từ người dùng
prompt = st.text_area("📝 Nhập mô tả hình ảnh:", height=150)

# Nút gửi yêu cầu tạo hình ảnh
if st.button("Tạo Ảnh 🚀"):
    if prompt.strip():
        st.info("⏳ Đang tạo hình ảnh, vui lòng chờ...")

        # Gửi request đến API
        payload = {"prompt": prompt}
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            image_url = response.json().get("image_url", None)

            if image_url:
                st.success("✅ Hình ảnh đã được tạo!")
                st.image(image_url, caption="Hình ảnh tạo từ AI", use_column_width=True)
            else:
                st.error("⚠️ API không trả về hình ảnh hợp lệ.")
        else:
            st.error("❌ Không thể tạo ảnh. Vui lòng kiểm tra API.")
    else:
        st.warning("⚠️ Vui lòng nhập mô tả hình ảnh!")

# Footer
st.markdown("---")
st.markdown("🚀 **Ứng dụng sử dụng mô hình Stable Diffusion 2.1**")
