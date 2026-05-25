"""
Tavily Web Search Assistant

A conversational AI assistant that provides comprehensive web search capabilities
using the Tavily Search API, designed specifically for AI agents.
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from strands import Agent
from strands.models import BedrockModel
from strands_tools import tavily

# Load environment variables
load_dotenv()

bedrock_model = BedrockModel(
    model_id="amazon.nova-micro-v1:0",
    region_name="us-east-1",
    temperature=0.3,
)


def create_tavily_search_agent():
    """Create a Tavily Web Search assistant agent."""
    
    # Verify API key is configured
    tavily_api_key = os.getenv("TAVILY_API_KEY")
    if not tavily_api_key:
        raise ValueError("TAVILY_API_KEY environment variable is required")
    
    # Configure Tavily tool
    tavily_tool = tavily
    
    return Agent(
        tools=[tavily_tool],
        model=bedrock_model,
        system_prompt=f"""You are a helpful web search assistant powered by Tavily Search API.

Current date: {datetime.now().strftime('%B %d, %Y')}

IMPORTANT: Be efficient with searches. Use only 1-2 search queries maximum per user question.

Your capabilities include:
- Comprehensive web search across the internet using Tavily's AI-optimized search
- Real-time, accurate, and factual results
- Cleaned and structured content specifically designed for AI agents

When users ask questions:
1. Use ONE targeted search query to find relevant information
2. Only make a second search if the first results are insufficient
3. Provide comprehensive answers based on the search results
4. Include source citations when relevant
5. Always mention the current date context when discussing "recent" information

Tavily provides high-quality, AI-optimized search results. Always aim for efficiency - avoid multiple redundant searches."""
    )

def main():
    """Main function to run the Tavily Web Search assistant."""
    
    try:
        # Create the agent
        agent = create_tavily_search_agent()
        
        print("🔍 Tavily Web Search Assistant")
        print("=" * 50)
        print("Ask me anything! I can search the web for you using AI-optimized search.")
        print("Examples:")
        print("- 'Search for recent AWS Lambda updates'")
        print("- 'What are the latest AI developments?'")
        print("- 'Find information about climate change research'")
        print("- 'Look up Python best practices for 2025'")
        print("Type 'quit' to exit.")
        
        # Interactive loop
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                print("🤖 Assistant:")
                response = agent(user_input)
                print(f"{response}")
                
            except KeyboardInterrupt:
                print("👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
            
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        print("Please check your TAVILY_API_KEY in the .env file")

if __name__ == "__main__":
    main()
