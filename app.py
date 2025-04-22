import streamlit as st
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define agents
web_search_agent = Agent(
    name="Web Agent",
    description="This is the agent for searching content from the web",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DuckDuckGo()],
    instructions="Always include the sources",
    show_tool_calls=True,
    markdown=True,
    debug_mode=True
)

finance_agent = Agent(
    name="Finance Agent",
    description="Your task is to find the financial information",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[YFinanceTools(
        stock_price=True,
        analyst_recommendations=True,
        company_info=True,
        company_news=True
    )],
    instructions=["Use tables for display the data"],
    show_tool_calls=True,
    markdown=True,
    debug_mode=True
)

agent_team = Agent(
    team=[web_search_agent, finance_agent],
    model=Groq(id="llama-3.3-70b-versatile"),
    instructions=["Always include sources", "Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
    debug_mode=True
)

# Streamlit UI
st.set_page_config(page_title="AI Agent Team", layout="wide")
st.title("💬 AI Agent Team")
st.write("Ask a question and let the agents work together to respond!")

query = st.text_input("Enter your query here", value="Summarize analyst recommendations for NVDA")

if st.button("Run Agent Team"):
    with st.spinner("Thinking..."):
        placeholder = st.empty()
        response = ""
        for chunk in agent_team.stream_response(query):
            response += chunk.content
            placeholder.markdown(response, unsafe_allow_html=True)