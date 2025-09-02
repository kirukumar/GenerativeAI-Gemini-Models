from urllib import response
from dotenv import load_dotenv
load_dotenv() ## loads all the environment variables from a .env file

import os
import streamlit as st
import google.generativeai as genai

## this is used to configure the api Key.
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("models/gemini-2.5-flash-lite")


def generate_response(prompt):
    response = model.generate_content(prompt)
    return response.text

## UI Settings
st.set_page_config(page_title="Text Speech Application", page_icon=":guardsman:", layout="wide")
st.header("Gemini AI Application")
user_input = st.text_input("Enter your prompt:")

generate_button = st.button("Ask Question")

if generate_button and user_input:
    response = generate_response(user_input)
    st.subheader("The Response is:")
    st.write(response)

