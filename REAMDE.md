Basic Flow

Agent receives a NEW service desk ticket (e.g., "Break-in at Wayne Tower #8")
Agent calls lookup_closed_tickets() - pulls ALL closed tickets
Agent does similarity search in-context on the ticket titles/descriptions
Agent finds the most similar past tickets
Agent analyzes those resolutions and suggests a solution