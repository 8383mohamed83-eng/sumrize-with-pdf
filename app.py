import streamlit as st
from groq import Groq
import PyPDF2
import io

st.title("Sumrizer")

client = Groq(api_key=st.secrets["API_KEY"])
st.title("Summarize")
uploaded_file = st.file_uploader("Upload your pdf", type=['pdf'])

if not uploaded_file is None:

    pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
    pdf_text = ""

    for page in pdf_reader.pages:
        pdf_text += page.extract_text() or ""
    if pdf_text.strip():
       st.info(f"text extracted from {len(pdf_reader.pages)} page")
       text_from_pdf = pdf_text
    else:
        st.warning("There is no text in your pdf")
        text_from_pdf = ""

else:
    text_from_pdf = ""







text = st.text_area("Write your text", height=200,value=text_from_pdf)

if st.button("Summarize"):
    if len(text.split()) < 10:
        st.warning("text is too short")
    else:
        with st.spinner("Summarizing..."):
            response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "You are a helpful assistant, summarize this text in the same language"}, {"role": "user", "content": text}])
        st.success(response.choices[0].message.content)
