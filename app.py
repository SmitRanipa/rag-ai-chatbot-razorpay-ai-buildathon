import os
import threading
import webbrowser
from flask import Flask, render_template, request, jsonify, session
import urllib.request
import time

# Import the RAG logic
import main as rag

app = Flask(__name__)
app.secret_key = "darshan-university-rag-chatbot-2026"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({"response": "Please type a question about Darshan University."})
    
    # Initialize session history if not present
    if 'history' not in session:
        session['history'] = []
    
    # Build a contextual search query using conversation history
    # This helps with follow-up questions like "And for MCA?" after asking about CSE placement
    search_query = user_message
    history = session['history']
    
    if len(history) > 0 and len(user_message.split()) < 8:
        # Short follow-up question — prepend context from previous question
        last_q = history[-1].get('question', '')
        search_query = f"{last_q} {user_message}"
    
    # Retrieve relevant chunks
    docs = rag.get_relevant_chunks(search_query)
    
    if not docs:
        answer = "I couldn't find relevant information about that in the Darshan University data. Could you try rephrasing your question?"
        # Save to history
        session['history'] = history[-4:] + [{'question': user_message, 'answer': answer}]
        session.modified = True
        return jsonify({"response": answer})
    
    # Build the prompt with conversation context
    if len(history) > 0:
        # Include last exchange for conversation continuity
        last_exchange = history[-1]
        context_prefix = f"Previous question: {last_exchange.get('question', '')}\nPrevious answer summary: {last_exchange.get('answer', '')[:200]}\n\nCurrent "
        prompt = rag.build_prompt(user_message, docs)
        # Insert conversation context into the prompt
        prompt = prompt.replace("QUESTION:", f"CONVERSATION CONTEXT:\n{context_prefix}\nQUESTION:")
    else:
        prompt = rag.build_prompt(user_message, docs)
    
    answer = rag.ask_ollama(prompt)
    
    # Save to history (keep last 5 exchanges)
    session['history'] = history[-4:] + [{'question': user_message, 'answer': answer}]
    session.modified = True
    
    return jsonify({"response": answer})

@app.route('/api/reset', methods=['POST'])
def reset_chat():
    """Reset the conversation history."""
    session.pop('history', None)
    return jsonify({"status": "ok"})

def open_browser():
    # Wait until the server is responsive
    url = "http://127.0.0.1:5000"
    for _ in range(10):
        try:
            urllib.request.urlopen(url)
            break
        except Exception:
            time.sleep(0.5)
    
    webbrowser.open_new(url)

if __name__ == '__main__':
    # Start browser auto-open in a background thread
    threading.Thread(target=open_browser, daemon=True).start()
    print("=" * 50)
    print("  Darshan University RAG Chatbot - Web UI")
    print(f"  Model: {rag.OLLAMA_MODEL}")
    print(f"  Chunks in DB: {rag.get_db_count()}")
    print("  URL: http://127.0.0.1:5000")
    print("=" * 50)
    app.run(host='127.0.0.1', port=5000)
