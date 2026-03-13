import streamlit as st
import agent

st.title("🏙️ Pecedung : Pemandu Cerdas Kota Bandung")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Ketik Di Sini"):
    model = agent.init_agent()
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = model.invoke({
        "messages" : st.session_state.messages
    })

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response['messages'][-1].content)

    st.session_state.messages.append({"role": "assistant", "content": response['messages'][-1].content})


    

