from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider
from datetime import datetime
from typing import Optional

# Ticket model
class Ticket(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    assigned_to: str = "Unassigned"
    status: str = "open"
    priority: str = "high"
    submitted_at: datetime = Field(default_factory=datetime.now)
    resolution: Optional[str] = None

# Agent setup
ollama_model = OpenAIChatModel(
    model_name="Mistral",
    provider=OllamaProvider(base_url="http://localhost:11434/v1")
)
agent = Agent(
    model=ollama_model,
    system_prompt=(
        "You are the Gotham Service Desk Assistant, integrated into the Batcomputer. "
        "Your job is to help the heroes, officers, and staff of Gotham City quickly "
        "and accurately manage service tickets."
    )
)

# Function to resolve a ticket
def resolve_ticket_with_agent(ticket: Ticket) -> Ticket:
    prompt = f"""
    Ticket ID: {ticket.id}
    Title: {ticket.title}
    Description: {ticket.description}
    Priority: {ticket.priority}
    Status: {ticket.status}
    Assigned to: {ticket.assigned_to}

    Provide a detailed resolution for this ticket.
    """
    result = agent.run_sync(prompt)
    ticket.resolution = result
    return ticket

def main():
    # Example usage
    current_ticket = Ticket(
        id=101,
        title="Break-in at Wayne Tower #11",
        description="Security alarms triggered on the 40th floor R&D section at 2:13 AM. Security footage shows three masked individuals accessing the prototype vault. They appear to have had access codes. No physical damage to entry points.",
        priority="critical"
    )

    resolved_ticket = resolve_ticket_with_agent(current_ticket)
    print(f"*********\nResolution:\n")
    print(resolved_ticket.resolution.output)

if __name__ == "__main__":
    main()
