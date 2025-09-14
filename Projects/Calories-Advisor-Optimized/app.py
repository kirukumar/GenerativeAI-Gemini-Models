## This is a LIM Model because we are working with the images

import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

load_dotenv()
genai.configure(api_key=os.getenv("GENAI_API_KEY"))


def get_gemini_response(prompt,image):
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    response = model.generate_content([prompt,image])
    return response.text

st.set_page_config(page_title="Calorie Advisor", page_icon=":shallow_pan_of_food:", layout="wide")
st.title("Calorie Advisor :shallow_pan_of_food:")
st.write("Upload an image of your meal, and get an estimate of its calorie content along with some healthy eating tips!")

uploaded_image = st.file_uploader("Choose an image of your meal", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption='Uploaded Meal Image', use_column_width=True)

submit_button = st.button("Get Calorie Estimate")

if submit_button:
    if uploaded_image is not None:
        with st.spinner("Analyzing the image and estimating calories..."):
            prompt = '''You are a nutrition expert. Analyze the image of the meal provided and estimate its calorie content.
            Provide a detailed breakdown of the ingredients you identify in the meal, their approximate quantities,
            and the total estimated calorie count. Additionally, offer some healthy eating tips related to the meal.
            Provide the calories count of the each item in the below format:
            Item 1: <calorie count>
            Item 2: <calorie count>
            
            '''
            try:
                response = get_gemini_response(prompt, image)
                st.subheader("Calorie Estimate and Healthy Eating Tips")
                st.write(response)
            except Exception as e:
                st.error(f"An error occurred while processing the image: {e}")
    else:
        st.error("Please upload an image of your meal to get a calorie estimate.")
