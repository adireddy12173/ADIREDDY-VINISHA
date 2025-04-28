from database import check_knowledge_base

# Agent Logic
def agent_respond(question):
    answer = check_knowledge_base(question)
    if answer:
        return answer, True
    else:
        return None, False

def update_agent_knowledge(question, answer):
    # Simple wrapper to update internal knowledge
    from database import add_to_knowledge_base
    add_to_knowledge_base(question, answer)
