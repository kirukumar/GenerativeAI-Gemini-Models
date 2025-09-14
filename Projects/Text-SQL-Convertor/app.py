from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai
import os
import sqlite3

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


## Function to load Google Gemini model
def get_gemini_response(prompt, question):
   model = genai.GenerativeModel("models/gemini-2.5-pro")
   response = model.generate_content([prompt, question])
   return response.text

## Function to execute a query and fetch results
def execute_query(query):
    connection = sqlite3.connect("example.db")
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    connection.commit()
    connection.close()
    return rows

st.set_page_config(page_title="Text to SQL Convertor", page_icon=":guardsman:", layout="wide")
st.title("Text to SQL Convertor :guardsman:")
st.write("Convert natural language text to SQL queries using Google Gemini model.")

prompt = """
        You are an expert SQL developer. Convert the following natural language question into a valid SQL query.
        Ensure the SQL query is syntactically correct and can be executed on a SQLite database.
        SQL Table has the following table users with column id, name, age.
        Remove all the markdown formatting and return only the SQL query.
        If the columns mentioned are not present in the table, tell not able to frame Query.
        For example:
        Get All Users -> SELECT * FROM users;
        Get Users older than 30 -> SELECT * FROM users WHERE age > 30;
        """

user_input = st.text_input("Enter your question:")

if st.button("Get Response"):
    if user_input:
        sql_query = get_gemini_response(prompt, user_input)
        st.subheader("Generated SQL Query:")
        st.code(sql_query, language="sql")
        
        try:
            results = execute_query(sql_query)
            st.subheader("Query Results:")
            if results:
                for row in results:
                    st.write(row)
            else:
                st.write("No results found.")
        except Exception as e:
            st.error(f"Error executing query: {e}")
    else:
        st.warning("Please enter a question to generate SQL query.")