# In-Memory DB Simulation
help_requests = {}  # request_id: {caller_id, question, status, answer}
knowledge_base = {}  # question: answer

def create_help_request(request_id, caller_id, question):
    help_requests[request_id] = {
        'caller_id': caller_id,
        'question': question,
        'status': 'Pending',
        'answer': None
    }

def get_pending_requests():
    return {rid: req for rid, req in help_requests.items() if req['status'] == 'Pending'}

def get_request_by_id(request_id):
    return help_requests.get(request_id)

def resolve_help_request(request_id, answer):
    if request_id in help_requests:
        help_requests[request_id]['status'] = 'Resolved'
        help_requests[request_id]['answer'] = answer

def check_knowledge_base(question):
    return knowledge_base.get(question)

def add_to_knowledge_base(question, answer):
    knowledge_base[question] = answer

def get_knowledge_base():
    return knowledge_base
