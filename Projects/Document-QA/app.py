import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS ##vector store db
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings ## vector store embedding technique
from dotenv import load_dotenv
import asyncio


load_dotenv()

## load the Groq API key from .env file
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

st.title("Document Q&A with Groq and Google Gemma Model")

llm = ChatGroq(groq_api_key=GROQ_API_KEY, model="Gemma-7b-it")


prompt = ChatPromptTemplate.from_template(
"""
Answer the question based on the context below. If the answer is not contained within the text below, say "I don't know".
Context: {context}
Question: {question}
Answer:
"""
)

def vector_embeddings():

    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    if "vectors" not in st.session_state:
        st.session_state.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        st.session_state.loader = PyPDFDirectoryLoader("./Test")
        st.session_state.documents = st.session_state.loader.load()
        st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.documents)
        st.session_state.vectors = FAISS.from_documents(st.session_state.final_documents, st.session_state.embeddings)

user_input = st.text_input("Ask a question about the documents:")

if st.button("Creating Vector DB"):
    with st.spinner("Creating..."):
        vector_embeddings()
        st.write(f"vector DB is Ready")
        
if user_input:
    document_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)
    retriever= st.session_state.vectors.as_retriever()
    retrieval_chain= create_retrieval_chain(retriever=retriever, llm_chain=document_chain)
    response = retrieval_chain.invoke({"question": user_input})
    st.write(response['answer'])
