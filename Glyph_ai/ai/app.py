import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain.schema import SystemMessage
import tempfile
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize embeddings outside the main function
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

if "flowmessage" not in st.session_state:
    st.session_state['flowmessage']=[
        SystemMessage(content="You are a Historical and archaeological assistant. Provide the best answer of the query as soon and as accurate as possible")
    ]

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        try:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                text += page.extract_text()
        except Exception as e:
            print(f"Error processing PDF: {e}")
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks,embeddings):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embeddings)
    vector_store.save_local("faiss_local")

def get_conversational_chain():
    prompt_template = """Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not provided in the context, just say, "answer is not available in the context", don't provide the wrong answer \n\n
    Context:\n{context}\n
    Question:\n{question}\n
    
    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question):
    try:
        new_db = FAISS.load_local("faiss_local", embeddings, allow_dangerous_deserialization=True)
        docs = new_db.similarity_search(user_question)
        chain = get_conversational_chain()
        response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
        st.write("Reply : ", response["output_text"])
    except FileNotFoundError:
        st.error("Faiss index file not found. Please check if the file exists.")
        st.stop()
def main():
    st.set_page_config("GLYPH AI")
    st.header("Chat with Glyph AI")

    user_question = st.text_input("Ask a Question")

    if user_question:
        user_input(user_question)
    
    with st.sidebar:
        st.title("Menu :")
        pdf_files = st.file_uploader("Upload your pdf files and click on the Submit Button & Process", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing ...."):
                if pdf_files is not None:
                    for pdf_file in pdf_files:
                        # Save the uploaded PDF file to a temporary location
                        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                            tmp_file.write(pdf_file.read())
                            pdf_path = tmp_file.name

                        raw_text = get_pdf_text([pdf_path])
                        text_chunks = get_text_chunks(raw_text)
                        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
                        get_vector_store(text_chunks,embeddings)
                        st.success("Done")

                        # Remove the temporary file after processing
                        os.unlink(pdf_path)
if __name__ == "__main__":
    main()