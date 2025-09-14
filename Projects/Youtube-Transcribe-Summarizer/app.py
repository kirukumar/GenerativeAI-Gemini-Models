import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
from dotenv import load_dotenv
import os
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_gemini_content(prompt,transcript_text):
    model = genai.GenerativeModel("models/gemini-2.5-pro")
    response = model.generate_content(prompt+transcript_text)
    return response.text

ytt_api = YouTubeTranscriptApi()

def extract_transcript_details(video_url):
    try:
        video_id = video_url.split("=")[1]
        transcript_list = ytt_api.fetch(video_id)
        transcript = ""
        for i in transcript_list:
            transcript += " " + i['text']

        return transcript
    except Exception as e:
        st.error(f"Error fetching transcript: {e}")
        return None

prompt = """You are a helpful assistant that summarizes YouTube video transcripts.
Given the transcript of a YouTube video, provide a concise summary highlighting the main points discussed in the video.
The summary should be clear and easy to understand, capturing the essence of the video's content. 
Please Provide the transcript text here: 
  """

st.title("YouTube Transcript Summarizer with Gemini")
st.write("Enter a YouTube video URL to get a summary of its transcript.")
video_url = st.text_input("YouTube Video URL")

if video_url:
     video_id = video_url.split("=")[1]
     st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", width=400)

if st.button("Get Summary"):
    if video_url:
         transcript_text = extract_transcript_details(video_url)
         if transcript_text:
            summary = generate_gemini_content(prompt, transcript_text)
            st.subheader("Video Transcript Summary:")
            st.write(summary)
    else:
        st.error("Please enter a valid YouTube video URL.")