import streamlit as st 
from chatbot_model import the_memory, the_conversation  

# Set the title of the Streamlit app
st.title("This is a Chatbot App") 

# Initialize the conversation memory if it doesn't exist in the session state
if 'memory' not in st.session_state: 
    st.session_state.memory = the_memory()

# Initialize the chat history if it doesn't exist in the session state
if 'chat_history' not in st.session_state: 
    st.session_state.chat_history = [] 

# Display the chat history in the Streamlit app
for message in st.session_state.chat_history: 
    with st.chat_message(message["role"]): 
        st.markdown(message["text"]) 

# Input field for the user to enter their message
input_text = st.chat_input("Powered by Bedrock and Claude") 

# If the user has entered a message
if input_text: 
    # Display the user's message in the chat
    with st.chat_message("user"): 
        st.markdown(input_text) 
    
    # Append the user's message to the chat history
    st.session_state.chat_history.append({"role": "user", "text": input_text}) 

    # Get the chatbot's response using the conversation function
    chat_response = the_conversation(input_text=input_text, memory=st.session_state.memory)
    
    # Display the chatbot's response in the chat
    with st.chat_message("assistant"): 
        st.markdown(chat_response) 
    
    # Append the chatbot's response to the chat history
    st.session_state.chat_history.append({"role": "assistant", "text": chat_response}) 
