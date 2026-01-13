from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from pprint import pprint


from init_agent import initialize_agent

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

def print_schema(messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
    tool = info.function_tools[0]
    print(tool.description)
    #> Get me foobar.
    print(tool.parameters_json_schema)
    """
    {
        'additionalProperties': False,
        'properties': {
            'a': {'description': 'apple pie', 'type': 'integer'},
            'b': {'description': 'banana cake', 'type': 'string'},
            'c': {
                'additionalProperties': {'items': {'type': 'number'}, 'type': 'array'},
                'description': 'carrot smoothie',
                'type': 'object',
            },
        },
        'required': ['a', 'b', 'c'],
        'type': 'object',
    }
    """
    return ModelResponse(parts=[TextPart('foobar')])

def main():
    # Initialize agent and deps, agent has tools registered
    agent, deps = initialize_agent(db_location="database/gotham_service_desk.db")

    # for tool_definition in agent.function_tools:
    #     print(f"Tool Name: {tool_definition.name}")
    #     print(f"Description: {tool_definition.description}")
    #     print(f"Parameters Schema: {tool_definition.parameters_json_schema}\n")

    ticket_id = 1
    prompt = f"""
    1. Get ticket {ticket_id} from the database. 
    2. Look up to see if there are similar tickets that have already been resolved.
    3. Generate a proposed solution for the ticket based on the description and similar tickets.
    4. Fill in the 'proposed_solution' field with your proposed solution.
    5. Update the ticket with the proposed solution. Update the status of the ticket to 'pending'
    """

    print("\n\n===================================")
    print(f"Asking agent to fetch, propose solution, and update ticket id: {ticket_id}...")
    print("===================================")

    ticket_result = agent.run_sync(prompt, deps=deps)

    print("\n" + "=" * 80)
    print("AGENT EXECUTION TRACE")
    print("=" * 80)

    for i, message in enumerate(ticket_result.all_messages(), 1):
        print(f"\n[{i}] {message.__class__.__name__}")
        print("-" * 80)
        pprint(vars(message), indent=2, width=100)
        print()

if __name__ == "__main__":
    main()

