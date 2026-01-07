from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.ollama import OllamaProvider
from datetime import datetime
from typing import Optional, List, Dict, Any
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

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

# FAISS setup
def load_vectorstore():
    """Load the FAISS vectorstore from disk."""
    try:
        embeddings_model = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            cache_folder="database/models"
        )

        # Load the FAISS index
        vectorstore = FAISS.load_local(
            "database/faiss_index",
            embeddings_model,
            allow_dangerous_deserialization=True
        )
        print(f"FAISS index loaded successfully with {vectorstore.index.ntotal} vectors")
        return vectorstore
    except Exception as e:
        print(f"Error loading FAISS index: {e}")
        print("Make sure to run database/setup_faiss.py first to create the index")
        return None

def find_similar_tickets(query: str, vectorstore=None, similarity_threshold: float = 0.6, top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Find tickets similar to the query using vector similarity search.

    Args:
        query: The query text to search for similar tickets
        vectorstore: Optional pre-loaded vectorstore (will load if None)
        similarity_threshold: Minimum similarity score to include results (0-1)
        top_k: Maximum number of results to return

    Returns:
        List of similar ticket metadata with their similarity scores
    """
    # Load vectorstore if not provided
    if vectorstore is None:
        vectorstore = load_vectorstore()

    try:
        # Perform similarity search with scores
        results = vectorstore.similarity_search_with_score(query, k=top_k)  # Get more results to filter

        # Filter by similarity threshold and take top_k
        filtered_results = []
        for doc, score in results:
            # Convert score to similarity (FAISS returns L2 distance, lower is better)
            # Converting to a similarity score between 0-1 where higher is better
            similarity = 1.0 / (1.0 + score)

            if similarity >= similarity_threshold:
                # Add similarity score to the metadata
                metadata = doc.metadata.copy()
                metadata["similarity"] = similarity
                filtered_results.append(metadata)

                if len(filtered_results) >= top_k:
                    break

        return filtered_results
    except Exception as e:
        print(f"Error finding similar tickets: {e}")
        return []

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
    similar_tickets = find_similar_tickets(f"Title: {ticket.title}, Description: {ticket.description}")

    similar_tickets_text = "\n".join(
        [f"- {t['title']} (similarity: {t['similarity']:.2f})" for t in similar_tickets]
    ) or "No similar tickets found."

    prompt = f"""
    Ticket ID: {ticket.id}
    Title: {ticket.title}
    Description: {ticket.description}
    Priority: {ticket.priority}
    Status: {ticket.status}
    Assigned to: {ticket.assigned_to}
    Similar tickets: {similar_tickets_text}

    Provide a detailed resolution for this ticket.
    """
    print("\n\n===================================")
    print("similar tickets:")
    for similar_ticket in similar_tickets:
        print(similar_ticket)    
    print("===================================")
                                           
    result = agent.run_sync(prompt)

    if isinstance(result, dict) and "output" in result:
        ticket.resolution = result["output"]
    elif hasattr(result, "output"):
        ticket.resolution = result.output
    else:
        ticket.resolution = str(result)  # fallback: just stringify

    return ticket

def main():
    current_ticket = Ticket(
        id=101,
        title="Break-in at Wayne Tower #11",
        description="Security alarms triggered on the 40th floor R&D section at 2:13 AM. Security footage shows three masked individuals accessing the prototype vault. They appear to have had access codes. No physical damage to entry points.",
        priority="critical",
        resolution=None
    )

    resolved_ticket = resolve_ticket_with_agent(current_ticket)
    print("\n\n===================================")
    print(f"Resolution:\n")
    print(resolved_ticket.resolution)
    print("===================================")


if __name__ == "__main__":
    main()
