import streamlit as st
import requests
import io
from PIL import Image
import os
from dotenv import load_dotenv

# Loading env
load_dotenv()
API_URL = os.getenv("GENERATE_IMAGE_API")
API_URL_IMAGE = os.getenv("API_CONTAINER")

if not API_URL:
    st.error("❌ Error: API_URL is not configured in the .env file.")
    st.stop()

# Component of page
st.title("🎨 Image Generator - Stable Diffusion")

prompt = st.text_area("📝 Enter image description:", height=150, placeholder="Let create your image! ")

if st.button("Generate Image 🚀"):
    with st.spinner("⏳ Processing..."):
        if prompt.strip():
            payload = {"prompt": prompt}
            response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                image_url = response.json().get("image_url", None)

                if image_url:
                    full_image_url = f"{API_URL_IMAGE}{image_url}"
                    
                    image_response = requests.get(full_image_url)

                    if image_response.status_code == 200:
                        image = Image.open(io.BytesIO(image_response.content))
                        st.success("✅ Image generated successfully!")
                        st.image(image, caption="AI-Generated Image", use_container_width =True)
                        image_bytes = io.BytesIO()
                        image.save(image_bytes, format="PNG")
                        image_bytes.seek(0)

                        st.download_button(
                            label="📥 Download Image",
                            data=image_bytes,
                            file_name="generated_image.png",
                            mime="image/png"
                        )
                    else:
                        st.error("⚠️ Failed to load the generated image.")
                else:
                    st.error("⚠️ API did not return a valid image URL.")
            else:
                st.error(f"❌ Unable to generate image. API Error: {response.status_code}")
        else:
            st.warning("⚠️ Please enter an image description!")

st.markdown("---")
st.markdown("🚀 **This application uses the Stable Diffusion 2.1 model.**")
