# XploreAI

Hướng dẫn chạy thử nghiệm trên local

**Bước 1:** Clone git `git clone https://github.com/Kevin310703/XploreAI`

**Bước 2:** Tạo branch  
- Tạo branch mới: `git checkout -b <tên branch>`
- Update branch: `git push -u origin <tên branch>`
  
**Bước 3:** Cài VirtualEnv 
- Vào cmd của thư mục chứa mã nguồn
- Chạy lệnh `pip install virtualenv`
- Tiếp theo tạo môi trường env `python -m venv xploreai-env`
- Truy cập môi trường env `xploreai-env\Scripts\activate`

**Bước 4:** Cài đặt các thư viện cần dùng: `pip install -r requirements.txt` vào môi trường sản phẩm env. Nếu gặp lỗi 'pkg_resources' thì chạy lệnh `pip install --upgrade setuptools` trước.

**Bước 5:** Chạy ứng dụng thử nghiệm trên local
- Truy cập vào thư mục "frontend" `cd frontend`
- Chạy lệnh `streamlit run streamlit_app.py`

 Hoặc có thể chạy thử nghiệm để người dùng trong cùng một mạng có thể truy cập:
 - Đầu tiên mở port trên máy và để port thường là 8080 (Có thể tùy chỉnh)
 - Sau đó chạy ứng dụng: `streamlit run home.py --server.port 8080`
 - Check ip: Bấm phím Windows, sau đó gõ cmd và check địa chỉ ip `ipconfig` (Window) hoặc `ifconfig` (Ubuntu). Sau đó tìm dòng có chứa `IPv4 Address`
 - Người dùng cùng mạng có thể truy cập: `<địa chỉ ipv4>:port` để xem giao diện ứng dụng streamlit


# Lưu ý:
- Phải tạo check branch trước khi pull hoặc push code `git checkout <tên branch>`
- Chạy terminal bằng quyền Admin trên Windows: Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
