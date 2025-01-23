from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as ai

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

API_KEY = "AIzaSyDyBf6TAhxoBMePIvZ4Vqn4WEomvilf3s0"
ai.configure(api_key=API_KEY)
model = ai.GenerativeModel("gemini-pro")
chat_instance = model.start_chat()

@app.route('/', methods=['GET', 'POST'])
def home():
    response_text = None
    if request.method == 'POST':
        user_message = request.form.get('message')
        if user_message:
            try:
                response = chat_instance.send_message(user_message)
                response_text = response.text
            except Exception as e:
                response_text = f"error: {e}"
        else:
            response_text = "Please enter a message"
            
    return render_template('index.html', response=response_text)    
    
@app.route('/chat', methods=['GET','POST'])
def chat_with_ai():
    user_message = request.json.get('message')
    
    if user_message:
        try:
            response = chat_instance.send_message(user_message)
            return jsonify({"response": response.text})
        except Exception as e:
            print("Error:", e)
            return jsonify({"error": "Failed to communicate with AI"}), 500
    else:
        return jsonify({"error": "No message provided"}), 400

if __name__ == "__main__":
    app.run(debug=True)
