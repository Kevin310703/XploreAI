import streamlit as st
import requests
from config import API_BASE_URL_BACKEND

# Lấy token từ URL
query_params = st.query_params
token = query_params.get("token", None)

st.title("✉️ Email Verification")

if token:
    with st.spinner("Verifying your email..."):
        response = requests.get(f"{API_BASE_URL_BACKEND}/verify-email/{token}/")

        if response.status_code == 200:
            st.success("✅ Your email has been verified successfully! You can now log in.")
        elif response.status_code == 400:
            st.warning("⚠️ Your email is already verified. Please log in.")
        else:
            st.error("❌ Verification failed. Invalid or expired token.")
else:
    st.error("❌ Invalid verification link.")
