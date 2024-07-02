from flask import Flask, render_template, request, jsonify
from controller import ChatbotController

app = Flask(__name__)
chatbot = ChatbotController(r'C:\Users\The Den\Desktop\New folder (4)\knowledge_base.json')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json['user_input']
    response = chatbot.process_user_input(user_input)
    return jsonify({'response': response})

@app.route('/set_context', methods=['POST'])
def set_context():
    context = request.json['context']
    chatbot.context = context
    return jsonify({'response': f"How may I help you with the {context} today?"})

if __name__ == '__main__':
    app.run(debug=True)