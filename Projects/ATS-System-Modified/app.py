import streamlit as st
import os

from dotenv import load_dotenv
import google.generativeai as genai
from PyPDF2 import PdfReader

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(prompt):
    model = genai.GenerativeModel("models/gemini-2.5-pro")
    response = model.generate_content(prompt)
    return response.text


def pdf_to_text(file):
    pdf = PdfReader(file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text() + "\n"
    return text


st.set_page_config(page_title="ATS System", page_icon=":robot_face:")
st.title("ATS System with Gemini 2.5 Pro")
st.write(
    "Upload a resume and job description to see how well the resume matches the job requirements"
)

resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_description = st.text_area("Enter Job Description")

if st.button("Evaluate"):
    if resume is not None and job_description.strip() != "":
        resume_text = pdf_to_text(resume)
        st.write("### Resume Text")
        st.write(resume_text)
        st.write("### Job Description")
        prompt = f"""
                You are an expert ATS (Applicant Tracking System) evaluator. Analyze the following resume against the job description and provide a comprehensive evaluation.

                JOB DESCRIPTION:
                {job_description}

                RESUME:
                {resume_text}

                Please provide your evaluation in the following format:

                CANDIDATE NAME: [Extract the candidate's name from the resume, if not found write "Name not found"]

                PERCENTAGE MATCH: [Provide a percentage from 0-100%]

                OVERALL SCORE: [Provide a score out of 10]

                STRENGTHS:
                • [List 3-5 key strengths and matching qualifications]

                AREAS FOR IMPROVEMENT:
                • [List 3-5 areas where the resume could be improved]

                MISSING SKILLS:
                • [List specific skills mentioned in job description but missing from resume]

                RECOMMENDATIONS:
                • [Provide 2-3 specific recommendations to improve the match]

                DETAILED EXPLANATION:
                [Provide a comprehensive explanation of why you gave this score, highlighting both positive aspects and areas of concern]

                Note: Be thorough and accurate in your analysis. Consider technical skills, experience level, education, and soft skills mentioned in both documents.
                """
        response = get_gemini_response(prompt)
        st.subheader("Evaluation Result")
        st.write(response)
    else:
        st.error("Please upload a resume and enter a job description.")
