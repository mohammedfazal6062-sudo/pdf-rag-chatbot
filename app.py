import os
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(page_title="PDF Study Chatbot", page_icon="📚")
st.header("Chat with your Study PDFs 📚")

pdf = st.file_uploader("Upload your PDF notes", type="pdf")

if pdf is not None:
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""

    st.success("PDF loaded! Ask any question below.")
    user_question = st.text_input("Ask a question about your PDF:")

    if user_question:
        prompt = f"Answer the question clearly based only on the following study notes:\n\n{text}\n\nQuestion: {user_question}"
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        st.write(response.text)
    
    