from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from werkzeug.datastructures import MultiDict
import os

# Import necessary libraries for text/audio processing and analysis
import openai
from openai import OpenAI
from audio_conversion import deepgram_transcribe_and_annotate, whisperx_transcribe_and_annotate

# Import api keys
from tokens import OPENAI_API_KEY

# Set up OpenAI API credentials
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Route for handling the index page.

    This function is responsible for handling both GET and POST requests to the root URL ("/").
    If the request method is POST, it processes the uploaded file and performs analysis on it.

    Parameters:
    - None

    Returns:
    - If the request method is GET, it renders the "index.html" template without any data.
    - If the request method is POST and a file is uploaded, it renders the "index.html" template with the processed conversation text and insights.

    Raises:
    - None

    Dependencies:
    - The function relies on the following modules and functions:
        - `secure_filename` from the `werkzeug.utils` module to securely generate a filename.
        - `request` from the `flask` module to handle the HTTP request.
        - `analyze_file` function to perform analysis on the conversation text.
        - `render_template` function to render the "index.html" template.
        - `deepgram_transcribe_and_annotate` function (if `api_type` is "deepgram") or `whisperx_transcribe_and_annotate` function (if `api_type` is "whisperx") to transcribe the audio file.

    Notes:
    - The function expects the uploaded file to be in either text or audio format.
    - The function saves the uploaded text file or audio file to the "UPLOAD_FOLDER" directory.
    """
    if request.method == 'POST':
        file = request.files['file']
        file_type = request.form['file_type']  # Get the file type (text or audio)
        api_type = request.form['api_type']

        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # If the uploaded file is a text file, read its content
            if file_type == 'text':
                with open(file_path, 'r', encoding='utf-8') as f:
                    conversation_text = f.read()

            # If the uploaded file is an audio file, transcribe it using WhisperX and read the annotated content
            if file_type == 'audio':
                if api_type=="deepgram":
                    conversation_text = deepgram_transcribe_and_annotate(audio_file=file_path)
                elif api_type=="whisperx":
                    conversation_text = whisperx_transcribe_and_annotate(audio_file=file_path)
            
            # Process the file (text) and perform analysis
            insights = analyze_file(conversation_text)

            return render_template('index.html', conversation_text=conversation_text , insights=insights)

    return render_template('index.html')

@app.route('/api', methods=['GET', 'POST'])
def analyse_api():
    #return request.get_data()
    """
    Route for uploading files and performing analysis.

    Returns:
        JSON response with insights if file upload and analysis are successful.
        HTTP 400 Bad Request if any required parameters are missing.
    """
    file = request.files.get('file')
    file_type = request.form.get('file_type')
    api_type = request.form.get('api_type')

    if not file or not file_type:
        return jsonify({'error': 'Missing required parameters' + str(file) + str(file_type)}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    if file_type == 'text':
        with open(file_path, 'r', encoding='utf-8') as f:
            conversation_text = f.read()

    elif file_type == 'audio':
        if api_type == "deepgram":
            conversation_text = deepgram_transcribe_and_annotate(audio_file=file_path)
        elif api_type == "whisperx":
            conversation_text = whisperx_transcribe_and_annotate(audio_file=file_path)
        else:
            return jsonify({'error': 'Invalid api_type'}), 400

    else:
        return jsonify({'error': 'Invalid file_type'}), 400

    insights = analyze_file(conversation_text)
    return jsonify({'conversation_text': conversation_text, 'insights': insights})


def analyze_file(conversation_text):
    """
    Analyzes a conversation text and provides sentiment and psychological insights derived from the conversation using openAI's GPT-3.5-turbo model.

    Parameters:
        conversation_text (str): The text of the conversation to be analyzed.

    Returns:
        list: A list of insights derived from the conversation. Each insight is a string containing information about a speaker's sentiment or behavior.
    """
    
    print("Analyzing conversation: " + conversation_text)

    client = OpenAI(
        api_key = OPENAI_API_KEY,
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"Analyse the following conversation and provide one short critical paragraph each for each speaker. In your paragraphs, provide sentiment or psychological insights derived from the conversation, some insights about speakers, analyze traits such as reliability, optimism, confidence, and courage. Offer deep insights about each speaker, such as favorite and least favorite topics, and create a personal profile with recommendations on how the user should interact with the speaker in future interactions. Assess the speakers' attitudes towards each other or any third person, answering common human questions like 'Did he like me?'' and 'Does he trust me?'. Please DO NOT provide summary of the overall conversation, key words, etc. Output should be related to sentimental analysis. :\n\n{conversation_text}",
            },
        ],
    )
    print(response.choices[0].message.content)

    insights = response.choices[0].message.content.strip().split('\n\n')

    return insights

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)