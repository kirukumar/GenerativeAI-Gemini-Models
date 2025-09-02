import os
from tkinter import Image
import streamlit as st
import google.generativeai as genai
from PIL import Image

from dotenv import load_dotenv
load_dotenv()



## this is used to configure the api Key.
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def generate_response(input,image):
    if input != "":
        response = model.generate_content([input,image])
    else :
        response = model.generate_content([image])

    return response.text

st.set_page_config(page_title="Gemini AI - Vision", page_icon=":guardsman:", layout="wide")
st.header("Gemini AI - Vision")
prompt = st.text_input("Enter your prompt:")

st.title("🖼️ Image Analysis with Gemini")
st.write("Upload an image and ask questions about it")

uploaded_file = st.file_uploader(
    "Choose an image...", 
    type=['png', 'jpg', 'jpeg', 'gif', 'webp']
)

if uploaded_file is not None:
       image = Image.open(uploaded_file)
       st.image(image, caption='Uploaded Image', use_column_width=True)

generate = st.button("Generate")

if generate:
    response = generate_response(prompt, image)
    st.subheader("The Response is:")
    st.write(response)
