from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("models/gemini-2.5-flash")

def generate_gemini_response(input_prompt,image,prompt):
    response = model.generate_content([input_prompt,image,prompt])
    return response.text






st.set_page_config(page_title="Invoice Extractor", page_icon=":guardsman:", layout="wide")

st.title("Invoice Extractor")
user_input = st.text_input("Enter message to extract information from invoice")
uploaded_file = st.file_uploader("Upload Invoice", type=["pdf", "jpg", "jpeg", "png"])
button = st.button("Extract Information")

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.subheader("Uploaded Invoice is:")
    st.image(image, caption='Uploaded Invoice', use_column_width=True)

input_prompt = f'''
You are a helpful assistant for extracting information from invoices. The user has uploaded an invoice image and provided the following message:

User Message: {user_input}

Please analyze the invoice and extract the relevant information.
'''

if button:
    response = generate_gemini_response(input_prompt,image,user_input)
    st.subheader("Extracted Information:")
    st.write(response)
