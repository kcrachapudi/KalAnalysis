import streamlit as st

if 'submitted' not in st.session_state:
    st.session_state.submitted = False

def submit():
    st.session_state.submitted = True
    st.write('The submit button was clicked.')
    
st.button('Submit', on_click=submit)

st.button('Do nothing')