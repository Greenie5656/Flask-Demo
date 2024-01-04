from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Retrieve API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set")

# Instantiate OpenAI client with the retrieved API key
client = OpenAI(api_key=api_key)

@app.route('/', methods=['GET'])  # Root URL
def index():
    return render_template('form.html')  # Render the form template

@app.route('/submit', methods=['POST'])
def handle_form_submission():
    prompt = request.form['prompt']
    try:
        response = client.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        # Adapt the following line based on the actual response structure
        image_url = response['data'][0]['url']
        return render_template('display_image.html', image_url=image_url)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app
