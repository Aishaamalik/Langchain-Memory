import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory
import os
from dotenv import load_dotenv

load_dotenv()

# Load API key from environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("GROQ API key not found in environment variable 'GROQ_API_KEY'. Please set it in your .env file.")
    st.stop()

# Initialize GROQ LLM with the API key
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.1-8b-instant",
    temperature=0.7,
    max_tokens=200
)

st.title("Memory Agent with Streamlit and LangChain")

if "memory" not in st.session_state:
    st.session_state.memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=2000)

memory = st.session_state.memory

conversation = ConversationChain(llm=llm, memory=memory)

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []

def get_text():
    input_text = st.text_input("You:", key="input")
    return input_text

user_input = get_text()

if user_input:
    # Get response from conversation chain
    response = conversation.predict(input=user_input)

    # Store the conversation in session state
    st.session_state.past.append(user_input)
    st.session_state.generated.append(response)

if st.session_state["generated"]:
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        st.markdown(f"**You:** {st.session_state['past'][i]}")
        st.markdown(f"**Agent:** {st.session_state['generated'][i]}")
