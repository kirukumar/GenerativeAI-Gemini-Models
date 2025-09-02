from dotenv import load_dotenv
load_dotenv() ## loads all the environment variables from a .env file

import google.generativeai as genai
import os
import streamlit as st

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("models/gemini-2.5-flash")
chat = model.start_chat(history=[])

def gemini_response(question):
    response = chat.send_message(question,stream=True)
    return response

if "chat History" not in st.session_state:
    st.session_state["chat History"] = []

st.set_page_config(page_title="Conversational Chat Bot", page_icon=":robot_face:", layout="wide")

st.header("Gemini Conversational AI Chat Bot")

user_input = st.text_input("Enter the prompt:")
submit_button = st.button("Ask Question")
st.subheader("The response from Gemini is:")

if submit_button and user_input:
    response = gemini_response(user_input)
    st.session_state["chat History"].append(("You",user_input))

    for chunk in response:
        st.session_state["chat History"].append(("Bot",chunk.text))
        st.write(chunk.text)

st.subheader("Chat History")
for chat in st.session_state["chat History"]:
    st.write(f"{chat[0]}: {chat[1]}")
