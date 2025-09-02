from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import os
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
import streamlit as st

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"));


def get_pdf_texts(pf_docs):
    text = ""
    for pdf in pf_docs:
        reader = PdfReader(pdf)
        for page in reader.pages:
            text += page.extract_text() + "\n"

    return text

def generate_chunks(texts):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(texts)
    return chunks

def generate_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_Template='''
    Answer the Question as detailed as Possible from the provided context, Make sure to provide all the details, if the answer is not
    present in the provide context just say, "answer is not available in the provided context", don't provide wrong answers.\n\n

    Context:\n {context}?\n
    Question:\n {question}\n

    Answer:
    '''

    model = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash",temperature=0.3)
    prompt = PromptTemplate(template=prompt_Template,input_variables=["context", "question"])
    chain = load_qa_chain(llm=model,chain_type="stuff", prompt=prompt)
    return chain

def answer_query(query):

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.load_local("faiss_index", embeddings,allow_dangerous_deserialization=True)
    chunks = vector_store.similarity_search(query)

    chain = get_conversational_chain()
    response = chain({"input_documents": chunks, "question": query})

    print(response)
    st.subheader("Answer of the Query:")
    st.write("Reply:",response["output_text"])


def main():
    st.set_page_config(page_title="DocGPT", page_icon=":books:")
    st.title("DocGPT :books:")

    with st.sidebar:
        st.header("Upload PDF Files")
        uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
        button = st.button("Process")
        if uploaded_files and button:
            with st.spinner("Processing"):
                pdf_text = get_pdf_texts(uploaded_files)
                text_chunks = generate_chunks(pdf_text)
                generate_vector_store(text_chunks)
                st.success("Files Processed Successfully")
        
    
    st.header("Ask Questions about your Documents")
    question = st.text_input("Enter your question:")
    submit_button = st.button("Submit")
    if submit_button:
        answer_query(question)

if __name__ == "__main__":
    main()
