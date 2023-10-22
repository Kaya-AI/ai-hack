from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.agents import create_csv_agent
from langchain.memory import ConversationBufferMemory
import os

memory = ConversationBufferMemory(memory_key="chat_history")

agent = create_csv_agent(
  ChatOpenAI(model="gpt-4", temperature=0, openai_api_key=os.environ["OPENAI_API_KEY"]),
  "permits-2020-onwards.csv",
  verbose=True,
  agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
  memory=memory
)

def ask_agent(question):
  memory.add_user_utterance(question)
  response = agent.generate_response(question, memory.get_conversation_history())
  memory.add_agent_utterance(response)
  return response