from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory
import os
from dotenv import load_dotenv

def initialize_llm():
    load_dotenv()
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API key not found in environment variable 'GROQ_API_KEY'. Please set it in your .env file.")
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model="llama-3.1-8b-instant",
        temperature=0.7,
        max_tokens=200
    )
    return llm

def create_memory(llm):
    return ConversationSummaryBufferMemory(llm=llm, max_token_limit=2000)

def create_conversation(llm, memory):
    return ConversationChain(llm=llm, memory=memory)

def get_response(conversation, user_input):
    # user_input may contain style instruction prepended
    return conversation.predict(input=user_input)
