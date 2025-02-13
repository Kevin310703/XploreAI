import streamlit as st
import requests
import io
from PIL import Image
from config import API_BASE_URL_BACKEND_SERVICE

if not API_BASE_URL_BACKEND_SERVICE:
    raise ValueError("🚨 API base url is not set in the environment variables!")

# Component of page
st.title("🎨 Image Generator - Stable Diffusion")

prompt = st.text_area("📝 Enter image description:", height=150, placeholder="Let create your image! ")

if st.button("Generate Image 🚀"):
    with st.spinner("⏳ Processing..."):
        if prompt.strip():
            payload = {"prompt": prompt}
            response = requests.post(f"{API_BASE_URL_BACKEND_SERVICE}/generate-image", json=payload)

            if response.status_code == 200:
                image_url = response.json().get("image_url", None)

                if image_url:
                    full_image_url = f"{API_BASE_URL_BACKEND_SERVICE}{image_url}"
                    
                    image_response = requests.get(full_image_url)

                    if image_response.status_code == 200:
                        image = Image.open(io.BytesIO(image_response.content))
                        st.success("✅ Image generated successfully!")
                        st.image(image, caption="XploreAI-Generated Image", use_container_width =True)
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
