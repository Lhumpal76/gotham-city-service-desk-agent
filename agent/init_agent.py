from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from pydantic_ai import Agent, ModelMessage, ModelResponse, TextPart
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.function import AgentInfo, FunctionModel
from agent.deps import AgentDeps
from pprint import pprint
import tools
import settings

# Ticket model
class Ticket(BaseModel):
    id: int
    title: str
    assigned_to: str = "Unassigned"
    description: Optional[str] = None
    status: str = "open"
    priority: str = "high"
    proposed_solution: Optional[str] = None
    resolution: Optional[str] = None

def initialize_agent(db_location: str):
    """
    Initialize the Gotham Service Desk Agent with the Ollama model and deps.

    Args:
        db_location (str): Path to the SQLite database for tickets.

    Returns:
        agent (Agent): Initialized Pydantic AI agent.
        deps (AgentDeps): Structured dependencies object to pass into run_sync.
    """
    # Set up deps
    deps = AgentDeps(db_location=db_location)

    # Load settings from settings.py
    llm = OpenAIChatModel(
        model_name=settings.MODEL_NAME,
        provider=OpenAIProvider(
            base_url=settings.BASE_URL,
            api_key=settings.API_KEY
        ),
    )

    # Create agent with tools
    agent = Agent(
        model=llm,
        deps_type=AgentDeps,
        tools=[tools.fetch_ticket],
        system_prompt=(
            "You are the Gotham Service Desk Assistant, integrated into the Batcomputer. "
            "Your job is to help the heroes, officers, and staff of Gotham City quickly "
            "and accurately manage service tickets.\n\n"
            "IMPORTANT: You have access to tools. Always use the appropriate tools when needed:\n"
            "- Use fetch_ticket to retrieve ticket details from the database\n"
            "- Use find_similar_tickets to search for related tickets using semantic search\n"
            "Always call these tools rather than making up information."
        ),
        output_type=Ticket
    )

    return agent, deps
