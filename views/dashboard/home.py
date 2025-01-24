import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import random

st.title("🚀 Welcome to Streamlit!")
st.write("An interactive dashboard showcasing various capabilities of Streamlit!")

# --- Sidebar for quick navigation ---
st.sidebar.header("🔍 Quick Access")
page = st.sidebar.radio("Select a feature", ["📊 Data Visualization", "🎲 Fun Tools", "🧠 AI Image Generator"])

# ---------------- SECTION 1: DATA VISUALIZATION ----------------
if page == "📊 Data Visualization":
    st.subheader("📊 Random Data Visualization")

    # Generate random data
    df = pd.DataFrame(np.random.randn(50, 3), columns=["A", "B", "C"])
    
    # Show table
    st.write("### Randomly Generated Data Table")
    st.dataframe(df)

    # Matplotlib Plot
    st.write("### Matplotlib Line Chart")
    fig, ax = plt.subplots()
    ax.plot(df.index, df["A"], marker="o", linestyle="-", color="b", label="A")
    ax.plot(df.index, df["B"], marker="s", linestyle="--", color="r", label="B")
    ax.set_title("Random Data Trends")
    ax.legend()
    st.pyplot(fig)

    # Plotly Chart
    st.write("### Interactive Plotly Scatter Chart")
    fig2 = px.scatter(df, x="A", y="B", color="C", title="Interactive Scatter Plot")
    st.plotly_chart(fig2)

# ---------------- SECTION 2: FUN TOOLS ----------------
elif page == "🎲 Fun Tools":
    st.subheader("🎲 Random Fun Tools")
    
    # Dice Roll
    if st.button("🎲 Roll a Dice"):
        dice_result = random.randint(1, 6)
        st.success(f"🎉 You rolled a {dice_result}!")

    # Number Guessing Game
    st.write("### 🎯 Guess a number between 1 and 10")
    guess = st.number_input("Enter your guess:", min_value=1, max_value=10, step=1)
    actual_number = random.randint(1, 10)
    
    if st.button("Check Guess"):
        if guess == actual_number:
            st.success("🎉 Correct! You guessed the right number!")
        else:
            st.error(f"❌ Wrong! The correct number was {actual_number}.")
