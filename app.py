from flask import Flask, render_template, request, jsonify
from openai import OpenAI  # Make sure to import OpenAI
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField  
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
client = OpenAI()  # Initialize the OpenAI client

app.config["SECRET_KEY"] = "andrewgreen"
app.config["UPLOAD_FOLDER"] = "static/files"

class UploadFileForm(FlaskForm):
    file = FileField("file")
    submit = SubmitField("Upload File")

@app.route('/')
def index():
    return render_template('form.html')  # Render the form template

@app.route('/test', methods=["GET", "POST"])
def test():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('index.html', filename=filename, form=form)
    return render_template('index.html', form=form )


@app.route('/submit', methods=['POST'])
def handle_form_submission():
    prompt = request.form['prompt']

    try:
        # Use the working code from sample.py for image generation
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        # Extract the image URL from the response
        image_url = response.data[0].url
        
        # Render the template to display the image
        return render_template('display_image.html', image_url=image_url)

    except Exception as e:
        # Return a JSON response if an error occurs
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
