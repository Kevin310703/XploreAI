import base64
import streamlit as st

def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Get base64 string of the banner image
banner_base64 = get_base64_of_bin_file("assets/image/xploreai_banner.jpg")

html_content = f"""
<style>
/* General page styling */
body {{
    background: #f0f2f6;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 0;
}}

/* Header with gradient background */
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

/* Banner image */
.banner-img {{
    width: 100%;
    border-radius: 15px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}}

/* Service cards using CSS Grid with 2 fixed columns */
.service-cards {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 2rem;
    margin: 2rem 0;
}}

/* Individual service card */
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

/* Project description */
.description {{
    font-size: 1.2rem;
    line-height: 1.6;
    text-align: center;
    margin: 2rem auto;
    max-width: 900px;
    color: #444;
}}

/* Start button */
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
    <div class="sub-title">AI-powered services: Language Translation, Image Generation, Text Summarization</div>
</div>

<!-- Banner image -->
<img class="banner-img" src="data:image/jpeg;base64,{banner_base64}" alt="XploreAI Banner" />

<!-- Service cards -->
<h2 style="text-align: center; margin-top: 2rem;">Our Services</h2>
<div class="service-cards">
    <div class="service-card">
        <h3>Language Translation</h3>
        <p>Quickly convert text between multiple languages, making global communication effortless.</p>
    </div>
    <div class="service-card">
        <h3>Image Generation</h3>
        <p>Create unique images based on your ideas using cutting-edge AI technology.</p>
    </div>
    <div class="service-card">
        <h3>Text Summarization</h3>
        <p>Condense long texts while retaining key information, saving valuable time.</p>
    </div>
    <div class="service-card">
        <h3>Question Answering</h3>
        <p>Get instant answers to your queries using AI, providing accurate and fast information retrieval.</p>
    </div>
</div>

<!-- Project description -->
<div class="description">
    XploreAI is a pioneering platform offering AI-powered services to optimize workflows and foster creativity. Let AI assist you in tackling challenges in the digital era!
</div>

<!-- "Get Started" Button -->
<div style="text-align: center;">
    <button class="start-button" onclick="window.location.reload()">Get Started Now</button>
</div>
"""

st.markdown(html_content, unsafe_allow_html=True)
