## LLM
## TOOL
## Agent
## Memory
## Streaming
## Web Interfaces

from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
import streamlit as st


Model = ChatGroq(model="openai/gpt-oss-20b",streaming=True)
Tavily = TavilySearch(max_results=5)

if "memory" not in st.session_state:
    st.session_state.memory = MemorySaver()
    st.session_state.history = []


agent = create_agent(
    model = Model,
    tools = [Tavily],
    checkpointer=st.session_state.memory,
    system_prompt="""
    You are an amazing Ai agent 
    use serch tools when you need to exteral verification
    get accuate answers and releavant answers
    """    
)
## Building interface
st.title("AI Chatbot💬")
st.subheader("chat faster than light⚡")
for message in st.session_state.history:
    role = message["role"]
    content = message["content"]
    st.chat_message(role).markdown(content)

query=st.chat_input("Ask anything")

if query:
    
    st.chat_message("user").markdown(query)
    st.session_state.history.append({"role":"user","content":query})

    response = agent.stream(
        {"messages":{"role":"user","content":query}},
        {"configurable":{"thread_id":"1"}},
        stream_mode="messages"
    )
    # answer=response["messages"][-1].content
    # st.chat_message("Ai").markdown(answer)

    ai_container = st.chat_message("ai")
    with ai_container:
        space=st.empty()
        message = ""

        for chunk in response:
            message = message + chunk[0].content
            space.write(message)        

    st.session_state.history.append({"role":"AI","content":message})