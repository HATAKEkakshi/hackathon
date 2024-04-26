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
    input_variables=['Prompt '],
    template="tell me about  {Prompt}"

)
#openai integration
llm=OpenAI(temperature=0.1)
chain=LLMChain(llm=llm,prompt=first_input_prompt,verbose=True,output_key='Description')

#second prompt template
second_input_prompt=PromptTemplate(
    input_variables=['Description'],
    template="What is the {Description} of the following text"

)
# chain 
chain2=LLMChain(llm=llm,prompt=second_input_prompt,verbose=True,output_key='important_events')
parent_chain=SimpleSequentialChain(chains=[chain,chain2],verbose=True)

#output
if input_text:
    st.write(parent_chain.run(input_text))