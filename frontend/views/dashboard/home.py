import base64
import streamlit as st

def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Get string base64 của ảnh banner
banner_base64 = get_base64_of_bin_file("assets/image/xploreai_banner.jpg")

html_content = f"""
<style>
/* Định dạng chung cho trang */
body {{
    background: #f0f2f6;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 0;
}}

/* Header với gradient nền */
.header {{
    text-align: center;
    padding: 60px 20px;
    background: linear-gradient(135deg, #FF6B6B, #C70039);
    color: white;
    border-bottom-left-radius: 50px;
    border-bottom-right-radius: 50px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 2rem;
    position: relative;
}}
.header .big-title {{
    font-size: 3.5rem;
    font-weight: bold;
    margin: 0;
    padding: 0;
}}
.header .sub-title {{
    font-size: 1.8rem;
    margin-top: 10px;
}}

/* Banner ảnh */
.banner-img {{
    width: 100%;
    border-radius: 15px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}}

/* Container các thẻ dịch vụ sử dụng CSS Grid với 2 cột cố định */
.service-cards {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 2rem;
    margin: 2rem 0;
}}

/* Mỗi thẻ dịch vụ */
.service-card {{
    background: white;
    border-radius: 15px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    padding: 2rem;
    text-align: center;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}}
.service-card:hover {{
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
}}
.service-card h3 {{
    font-size: 1.5rem;
    color: #333;
    margin-bottom: 1rem;
}}
.service-card p {{
    font-size: 1rem;
    color: #555;
}}

/* Mô tả dự án */
.description {{
    font-size: 1.2rem;
    line-height: 1.6;
    text-align: center;
    margin: 2rem auto;
    max-width: 900px;
    color: #444;
}}

/* Nút Bắt đầu */
.start-button {{
    display: block;
    width: 220px;
    margin: 3rem auto;
    padding: 0.8rem;
    background-color: #FF4C4C;
    color: white;
    border: none;
    border-radius: 30px;
    font-size: 1.2rem;
    cursor: pointer;
    text-align: center;
    transition: background-color 0.3s ease;
}}
.start-button:hover {{
    background-color: #A80000;
}}
</style>

<!-- Header -->
<div class="header">
    <div class="big-title">XploreAI</div>
    <div class="sub-title">Ứng dụng AI đa dịch vụ: Dịch ngôn ngữ, Tạo hình ảnh, Tóm tắt văn bản</div>
</div>

<!-- Banner ảnh -->
<img class="banner-img" src="data:image/jpeg;base64,{banner_base64}" alt="Banner XploreAI" />

<!-- Các thẻ dịch vụ -->
<h2 style="text-align: center; margin-top: 2rem;">Các Dịch Vụ của Chúng Tôi</h2>
<div class="service-cards">
    <div class="service-card">
        <h3>Dịch Ngôn Ngữ</h3>
        <p>Chuyển đổi văn bản nhanh chóng giữa các ngôn ngữ, giúp giao tiếp toàn cầu dễ dàng hơn.</p>
    </div>
    <div class="service-card">
        <h3>Tạo Hình Ảnh</h3>
        <p>Sáng tạo hình ảnh độc đáo dựa trên ý tưởng của bạn thông qua công nghệ AI tiên tiến.</p>
    </div>
    <div class="service-card">
        <h3>Tóm Tắt Văn Bản</h3>
        <p>Rút gọn nội dung văn bản dài, giữ lại những thông tin cốt lõi quan trọng, tiết kiệm thời gian hiệu quả.</p>
    </div>
    <div class="service-card">
        <h3>Trả Lời Câu Hỏi</h3>
        <p>Giải đáp mọi thắc mắc của bạn với trí tuệ nhân tạo, hỗ trợ tìm kiếm thông tin nhanh chóng và chính xác.</p>
    </div>
</div>

<!-- Mô tả dự án -->
<div class="description">
    XploreAI là nền tảng tiên phong cung cấp các dịch vụ trí tuệ nhân tạo, giúp bạn tối ưu hóa quy trình làm việc và khám phá những sáng tạo mới. Hãy để AI hỗ trợ bạn giải quyết các thách thức trong thời đại số!
</div>

<!-- Nút "Bắt đầu ngay" -->
<div style="text-align: center;">
    <button class="start-button" onclick="window.location.reload()">Bắt đầu ngay</button>
</div>
"""

st.markdown(html_content, unsafe_allow_html=True)
