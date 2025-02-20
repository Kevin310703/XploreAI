import streamlit as st
import requests
import io
from PIL import Image
from config import API_BASE_URL_BACKEND_SERVICE, API_BASE_URL_BACKEND_STATIC_FILE

if not API_BASE_URL_BACKEND_SERVICE:
    raise ValueError("🚨 API base url is not set in the environment variables!")

if "generated_image" not in st.session_state:
    st.session_state.generated_image = None

def clear_generated_image():
    st.session_state.generated_image = None

# Component of page
with st.form("image_generator_form", enter_to_submit =True, border=False):
    st.title("🎨 Image Generator")
    with st.expander("ℹ️ How to Use", expanded=False):
        st.markdown("""
            🔹 **Step 1:** Enter an image description in the text box below.  
            🔹 **Step 2:** Click **"Generate Image 🚀"** to start the generation process.  
            🔹 **Step 3:** The generated image will be displayed and available for download.  

            ⚠️ **Note:**  
            - Use clear and detailed descriptions for better image generation.  
            - Ensure you are logged in and have a valid access token.  
            - If the response takes too long, your connection or internet stability.  
        """)

    prompt = st.text_area("📝 Enter image description:", height=150, placeholder="Let create your image! ")

    submitted = st.form_submit_button("Generate Image 🚀")
    if submitted:
        with st.spinner("⏳ Processing..."):
            if prompt.strip():
                payload = {"prompt": prompt}
                response = requests.post(f"{API_BASE_URL_BACKEND_SERVICE}/generate-image/", json=payload)

                if response.status_code == 200:
                    image_url = response.json().get("image_url", None)

                    if image_url:
                        full_image_url = f"{API_BASE_URL_BACKEND_STATIC_FILE}{image_url}"
                        
                        image_response = requests.get(full_image_url)

                        if image_response.status_code == 200:
                            image = Image.open(io.BytesIO(image_response.content))
                            st.success("✅ Image generated successfully!")
                            st.image(image, caption="XploreAI-Generated Image", use_container_width =True)

                            # Lưu ảnh vào session_state để có thể download bên ngoài form
                            image_bytes = io.BytesIO()
                            image.save(image_bytes, format="PNG")
                            image_bytes.seek(0)
                            st.session_state.generated_image = image_bytes
                        else:
                            st.error("⚠️ Failed to load the generated image.")
                    else:
                        st.error("⚠️ API did not return a valid image URL.")
                else:
                    st.error(f"❌ Unable to generate image. API Error: {response.status_code}")
            else:
                st.warning("⚠️ Please enter an image description!")

if st.session_state.generated_image:
    st.download_button(
        label="📥 Download Image",
        data=st.session_state.generated_image,
        file_name="generated_image.png",
        mime="image/png",
        on_click=clear_generated_image,
    )
    
st.markdown("---")
st.markdown("🚀 **© 2025 X-OR AI GENERATIVE**")
