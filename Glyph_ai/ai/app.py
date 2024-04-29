##conversional  q&a chatbot
import streamlit as st
from langchain.schema import HumanMessage,SystemMessage,AIMessage
from langchain_community.chat_models import ChatOpenAI

##streamlit ui
st.set_page_config(page_title="Glyph Ai ")
st.header("Hello, I'm Glyph  How can I help you ?")

from dotenv import load_dotenv # type: ignore
load_dotenv()
import os
chat=ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"),temperature=0.5)
if 'flowmessage' not in st.session_state:
    st.session_state['flowmessage']=[
        SystemMessage(content="You are an Archeologist Researcher and Help people Decoding the manuscript and scriots")
        ]
##function to load opeai 
def get_openai_response(question):
    st.session_state['flowmessage'].append(HumanMessage(content=question))
    answer=chat(st.session_state['flowmessage'])
    st.session_state['flowmessage'].append(AIMessage(content=answer.content))
    return answer


input=st.text_input("Input : ",key="input")
response=get_openai_response(input)
submit=st.button("Ask the question")
#if ask button is clicked

if submit:
    st.subheader("The Response is")
    st.write(response)
