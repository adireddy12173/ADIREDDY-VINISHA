from flask import Flask, request, jsonify, render_template, redirect
from database import create_help_request, get_pending_requests, resolve_help_request, get_request_by_id, add_to_knowledge_base, get_knowledge_base
from agent import agent_respond, update_agent_knowledge
import uuid

app = Flask(__name__)

# Simulated Incoming Call
@app.route('/incoming_call', methods=['POST'])
def incoming_call():
    data = request.json
    question = data.get('question')
    caller_id = data.get('caller_id')
    
    response, knows_answer = agent_respond(question)
    if knows_answer:
        print(f"[AI Response to {caller_id}]: {response}")
        return jsonify({'status': 'answered', 'response': response})
    else:
        print(f"[AI to {caller_id}]: Let me check with my supervisor and get back to you.")
        request_id = str(uuid.uuid4())
        create_help_request(request_id, caller_id, question)
        print(f"[Text to Supervisor]: Hey, I need help answering: '{question}' (Request ID: {request_id})")
        return jsonify({'status': 'escalated', 'request_id': request_id})

# Supervisor Dashboard
@app.route('/dashboard')
def dashboard():
    requests = get_pending_requests()
    return render_template('dashboard.html', requests=requests)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    request_id = request.form.get('request_id')
    answer = request.form.get('answer')
    
    help_request = get_request_by_id(request_id)
    if help_request:
        caller_id = help_request['caller_id']
        resolve_help_request(request_id, answer)
        update_agent_knowledge(help_request['question'], answer)
        print(f"[AI Follow-up to {caller_id}]: {answer}")
        return redirect('/dashboard')
    return "Request not found", 404

# View Learned Knowledge
@app.route('/knowledge_base')
def knowledge_base():
    kb = get_knowledge_base()
    return render_template('knowledge_base.html', knowledge=kb)

if __name__ == '__main__':
    app.run(debug=True)
