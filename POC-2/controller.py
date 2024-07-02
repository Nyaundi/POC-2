from openai import OpenAI
import json
import re
from multiprocessing import context

class ChatbotController:
    def __init__(self, knowledge_base_path):
        self.knowledge_base = self.load_knowledge_base(knowledge_base_path)
        self.context = None
        self.session_active = False
        self.client = OpenAI(api_key='sk-proj-nHzSrLZEbtqoHzOjDxKMT3BlbkFJCBmlQhoHAOCJCn0NoAON')

    def load_knowledge_base(self, path):
        with open(path, 'r') as file:
            return json.load(file)

    def start_new_session(self):
        self.session_active = True
        self.context = None
        return "Hello! I am Captain AI, how can I help you today?"

    def end_session(self):
        self.session_active = False
        self.context = None

    def process_user_input(self, user_input):
        if not self.session_active:
            if user_input.lower() in ['hi', 'hello']:
                self.start_new_session()
                return "Hello! I am Captain AI, how can I help you today??"
            else:
                return "Please start a new session by saying 'hi' or 'hello'."

        if user_input.lower() in ['end', 'quit', 'bye', 'thank you']:
            self.end_session()
            return "Thank you for using our service. If you have any more questions, please don't hesitate to ask."

        if user_input.lower() in ['hi', 'hello']:
            self.start_new_session()
            return "Starting a new session. How can I help you today?"

        if not self.context:
            context = self.identify_context(user_input)
            if context:
                self.context = context
                return self.generate_response(user_input)
            else:
                return "Which part of the boat are you having a problem with?"
        else:
            if self.match_context(user_input):
                return self.generate_response(user_input)
            else:
                new_context = self.identify_context(user_input)
                if new_context:
                    self.context = new_context
                    return self.generate_response(user_input)
                else:
                    return "I'm not sure which part you're referring to. Could you please specify the part you're having issues with?"

    def identify_context(self, user_input):
        parts = ['generator', 'air conditioner', 'heater', 'bow thruster', 'vacuflush', 'media master', 
                 'bilge pump', 'seakeeper', 'toilet', 'engine']
        
        for part in parts:
            if part in user_input.lower():
                return part
        return None

    def match_context(self, user_input):
        return self.identify_context(user_input) == self.context

    def generate_response(self, user_input):
        model = self.select_model()
        if model:
            prompt = self.create_prompt(user_input, model)
            return self.call_openai_api(prompt)
        else:
            return "I'm sorry, but I don't have enough information to respond to this query. Could you please provide more details or ask about a different part?"

    def select_model(self):
        if self.context:
            for key in self.knowledge_base.keys():
                if self.context in key.lower():
                    return self.knowledge_base[key]
        return None

    def create_prompt(self, user_input, model):
        return f"Context: {self.context}\nUser Query: {user_input}\nKnowledge Base: {model[:1000]}\nResponse:"

    def call_openai_api(self, prompt):
        try:
            response = self.client.completions.create(
                model="gpt-3.5-turbo-instruct",
                prompt=prompt,
                max_tokens=150
            )
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return "I'm sorry, but I encountered an error while processing your request. Please try again later."

    def set_context(self, context):
        self.context = context
        return f"How may I help you with the {context} today?"