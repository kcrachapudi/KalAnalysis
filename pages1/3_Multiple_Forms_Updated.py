import streamlit as st
import streamlit_ext as ste

st.title("Two Forms on a Single Page")
if 'initiated' not in st.session_state:
    st.session_state.initiated = False

if 'stage' not in st.session_state:
    st.session_state.stage = 'stage1'

if 'con1' not in st.session_state:
    st.session_state.con1 = st.empty()

st.session_state.name = st.sidebar.text_input("Enter your name")
st.session_state.age = st.sidebar.text_input("Enter your age")

def ProcessStage1():
    st.write(f"Stage 1 Processed! Name: {st.session_state.name}, Age: {st.session_state.age}")
    
btnProcessStage1 = st.sidebar.button("ProcessStage1", on_click=ProcessStage1)

st.session_state.bank = st.sidebar.text_input("Enter your Bank")
st.session_state.balance = st.sidebar.text_input("Enter your Balance")

def ProcessStage2():
    st.write(f"Stage 2 Processed! Bank: {st.session_state.bank}, Balance: {st.session_state.balance}")

btnProcessStage2 = st.sidebar.button("ProcessStage2", on_click=ProcessStage2)



