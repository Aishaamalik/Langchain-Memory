import streamlit as st
import base64
from backend import initialize_llm, create_memory, create_conversation, get_response
import time

st.set_page_config(page_title="Chat bot", layout="wide")

def set_bg_with_overlay(img_path, overlay_rgba="rgba(0,0,0,0.45)"):
    with open(img_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient({overlay_rgba}, {overlay_rgba}), url("data:image/png;base64,{b64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: white;
        }}
        .stApp .css-1d391kg {{ /* container text background tweak (class may vary) */
            background: rgba(255,255,255,0.0);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg_with_overlay("pic1.jpg", overlay_rgba="rgba(0,0,0,0.5)")

try:
    llm = initialize_llm()
except ValueError as e:
    st.error(str(e))
    st.stop()

title_placeholder = st.empty()
title_text = "Memory Agent with Streamlit and LangChain"
displayed_text = ""

for char in title_text:
    displayed_text += char
    title_placeholder.title(displayed_text)
    time.sleep(0.05)

style_option = st.sidebar.selectbox(
    "Select response style:",
    options=["professional", "casual", "gen-z style"],
    index=0,
    help="Choose the tone style for the agent's response"
)

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
    # Append style instruction to user input
    style_instruction = f"Respond in a {style_option} tone."
    styled_input = f"{style_instruction}\nUser: {user_input}"

    # Get response from conversation chain
    response = get_response(conversation, styled_input)

    # Store the conversation in session state
    st.session_state.past.append(user_input)
    st.session_state.generated.append(response)

if st.session_state["generated"]:
    for i in range(len(st.session_state["generated"])):
        with st.chat_message("user"):
            st.write(st.session_state['past'][i])
        with st.chat_message("assistant"):
            st.write(st.session_state['generated'][i])
