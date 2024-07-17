from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain_aws import ChatBedrock

# Function to initialize the chatbot with specific settings
def my_chatbot():
    # Creating a ChatBedrock instance with given credentials and model settings
    my_llm = ChatBedrock(
        credentials_profile_name='default',
        model_id='anthropic.claude-3-haiku-20240307-v1:0',
        model_kwargs={
            "max_tokens": 300,  # Maximum number of tokens in the response
            "temperature": 0.1,  # Controls the randomness of the response
            "top_p": 0.9,  # Controls the diversity of the response
            "stop_sequences": ["\n\nHuman:"]  # Sequence that stops the response generation
        }
    )
    return my_llm

# Function to create a memory buffer for the conversation
def the_memory():
    # Initialize the chatbot
    llm_data = my_chatbot()
    # Create a memory buffer with a maximum token limit
    memory = ConversationSummaryBufferMemory(llm=llm_data, max_token_limit=300)
    return memory

# Function to handle the conversation using the memory and the chatbot
def the_conversation(input_text, memory):
    # Initialize the chatbot again (consider reusing the instance from `the_memory` to avoid redundant initialization)
    llm_chain_data = my_chatbot()
    # Create a ConversationChain with the chatbot and memory, and enable verbose logging
    llm_conversation = ConversationChain(llm=llm_chain_data, memory=memory, verbose=True)

    # Invoke the conversation chain with the input text
    chat_reply = llm_conversation.invoke(input_text)
    # Return the response from the conversation
    return chat_reply['response']
