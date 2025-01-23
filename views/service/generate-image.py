import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_URL = os.getenv("GENERATE_IMAGE_API")

if not API_URL:
    st.error("❌ Error: API_URL is not configured in the .env file.")
    st.stop()

st.title("🎨 AI Image Generator - Stable Diffusion")

prompt = st.text_area("📝 Enter image description:", height=150)

if st.button("Generate Image 🚀"):
    if prompt.strip():
        st.info("⏳ Generating image, please wait...")

        # API Request
        payload = {"prompt": prompt}
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            image_url = response.json().get("image_url", None)

            if image_url:
                st.success("✅ Image generated successfully!")
                st.image(image_url, caption="AI-Generated Image", use_column_width=True)
            else:
                st.error("⚠️ API did not return a valid image.")
        else:
            st.error("❌ Unable to generate image. Please check the API.")
    else:
        st.warning("⚠️ Please enter an image description!")

st.markdown("---")
st.markdown("🚀 **This application uses the Stable Diffusion 2.1 model.**")
