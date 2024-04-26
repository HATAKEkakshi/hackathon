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

