# Importing necessary modules from the autogen package
import autogen
from autogen.agentchat.contrib.agent_builder import AgentBuilder

# Path to the configuration file
config_path = 'OAI_CONFIG_LIST.json'

# Loading the configuration list from the JSON file
config_list = autogen.config_list_from_json(config_path)

# Default configuration for the language learning model (LLM)
# Here, 'temperature' is set to 0 for deterministic output
default_llm_config = {'temperature': 0}

# Initializing the AgentBuilder with the given configuration path
builder = AgentBuilder(config_path=config_path)

# Defining the new task for the agents
# In this case, assisting with creating a simple snake game
building_task = "help me with creating a simple snake game"

# Building agents using the defined task and default LLM configuration
agent_list, agent_configs = builder.build(building_task, default_llm_config)

# Setting up a group chat with the built agents, initializing with no messages and a maximum of 12 rounds
group_chat = autogen.GroupChat(agents=agent_list, messages=[], max_round=12)

# Initializing the Group Chat Manager with the group chat and LLM configurations
manager = autogen.GroupChatManager(groupchat=group_chat, llm_config={"config_list": config_list, **default_llm_config})

# Initiating the chat with the first agent in the list
# The agent starts by providing assistance in creating a simple snake game
agent_list[0].initiate_chat(
    manager, 
    message="help me with creating a simple snake game"
)
