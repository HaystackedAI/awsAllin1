from strands import Agent, tool
from strands.models import BedrockModel
from strands_tools import calculator

# Define a custom weather tool
@tool
def weather():
    """Get the weather"""
    return "sunny"


bedrock_model = BedrockModel(
    model_id="amazon.nova-micro-v1:0",
    region_name="us-east-1",
    temperature=0.3,
)

# Initialize the agent with tools
agent = Agent(
    tools=[calculator, weather],
    model=bedrock_model,
    system_prompt="You're a helpful assistant. You can perform simple math and tell the weather."
)

response = agent("What is the weather today?")
print(response)