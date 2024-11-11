import streamlit as st

st.title('Chat with Llama Lingo')
st.header('Take a picture of your surroundings, and chat with Llama Lingo!')


enable = st.checkbox("Enable camera")
picture = st.camera_input("Take a picture", disabled=not enable)

if picture:
    st.image(picture)

st.session_state.picture = picture


if st.button("Chat with Llama Lingo!"):
    st.switch_page("pages/converse.py")