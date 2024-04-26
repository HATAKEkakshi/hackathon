##integrate our code with Openai api
import os
from constants import openai_key
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

from langchain.chains import SimpleSequentialChain
from langchain.chains import SequentialChain


import streamlit as st
os.environ["OPENAI_API_KEY"]=openai_key


st.title("Glyph")
input_text=st.text_input("How can i help you")

#Prompt Template

first_input_prompt=PromptTemplate(
    input_variables=['Word '],
    template="tell me about  {Word}"

)
llm=OpenAI(temperature=0.8)
chain=LLMChain(llm=llm,prompt=first_input_prompt,verbose=True,output_key='Description')

if input_text:
    st.write(chain.run(input_text))