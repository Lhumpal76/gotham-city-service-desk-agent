from pydantic import BaseModel

class AgentDeps(BaseModel):
    """
    Structured dependencies/configuration for Pydantic AI agents.

    Attributes:
        db_location (str): Path to the SQLite database used by tools.
        readonly (bool): Optional flag to indicate read-only access. Defaults to True.

    Notes:
        This object is passed to the agent at runtime via the `deps` argument.
        Every tool that uses `RunContext[AgentDeps]` will have access to these fields
        through `ctx.deps`.
    """
    db_location: str
    readonly: bool = True
