import streamlit as st
from backend import initialize_llm, create_memory, create_conversation, get_response

try:
    llm = initialize_llm()
except ValueError as e:
    st.error(str(e))
    st.stop()

st.title("Memory Agent with Streamlit and LangChain")

if "memory" not in st.session_state:
    st.session_state.memory = create_memory(llm)

memory = st.session_state.memory

if "conversation" not in st.session_state:
    st.session_state.conversation = create_conversation(llm, memory)

conversation = st.session_state.conversation

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
    response = get_response(conversation, user_input)

    # Store the conversation in session state
    st.session_state.past.append(user_input)
    st.session_state.generated.append(response)

if st.session_state["generated"]:
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        st.markdown(f"**You:** {st.session_state['past'][i]}")
        st.markdown(f"**Agent:** {st.session_state['generated'][i]}")
