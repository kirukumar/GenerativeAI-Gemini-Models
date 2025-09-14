import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import pdf2image ## Requires Poppler to be installed in the machine
import io
import base64

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(prompt, pdf_content,question):
    model = genai.GenerativeModel("models/gemini-2.0-flash-lite")
    response = model.generate_content([prompt, pdf_content[0], question])
    return response.text

def input_pdf_setUp(file):
    if file is not None:

        images = pdf2image.convert_from_bytes(file.read())
        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode("utf-8"),
            }
        ]

        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

st.set_page_config(page_title="ATS System using Gemini-2.5-Pro", layout="wide")
st.title("ATS System using Gemini-2.5-Pro")
st.write("Upload a resume and job description to analyze candidate fit.")

user_input= st.text_area("Enter your Job Description here:", height=100)
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    st.write("Resume uploaded successfully.")


submit_button1 = st.button("Tell me about the resume")
submit_button2 = st.button("Percentage Match")

input_prompt1 = '''
You are a experienced HR Professional with tech expertize in the field of IT recruitment with any one of the role related to data science or Full stack Development or AI Development.
Analyze the resume provided and give a detailed summary of the candidate's skills, experience, and suitability for a tech role. Highlight key strengths and any potential red flags.
Match the resume against the job description provided and provide the details.
'''

input_prompt2 = '''
You are a experienced ATS System(ATS) with tech expertize in the field of IT recruitment with any one of the role related to data science or Full stack Development or AI Development.
Compare the resume with the job description and provide a percentage match score along with areas of improvement and key skills missed.
Match the resume against the job description provided and provide the details.

The output should be in the following format:
Percentage Match: XX%\n
Areas of Improvement:\n
Job role match:

'''

if submit_button1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setUp(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, user_input)
        st.subheader("Resume Analysis")
        st.write(response)

if submit_button2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setUp(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, user_input)
        st.subheader("Percentage Match")
        st.write(response)





