import streamlit as st

st.title("Mphasis Practice")
st.header("Welcome to the Mphasis Practice")
st.write("Take a look on my first creation of streamlit")

name = st.text_input("Enter your name:", placeholder="Enter your name here")
if st.button("Say Hello"):
    if name == "":
        st.warning("Please enter your name and click on say hello button", icon="⚠️")
    else:
        st.write(f"Hello, {name}!")

age = st.slider("Select your age:", 1, 100, 25)
st.write(f"Your age is {age}")