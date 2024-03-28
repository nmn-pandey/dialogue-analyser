# Dialogue Analysis Project

This project is a web application built with Flask that allows users to upload text or audio files containing dialogues or conversations. The application then analyzes the content and provides sentiment and psychological insights for each speaker involved in the conversation.

**Live Preview Here**: https://dialogue-analyser-api-btkt3vr5aa-uc.a.run.app 

## Features

- Upload text or audio files containing dialogues or conversations.
- Transcribe audio files using either Deepgram API or WhisperX (open-source diarization/transcription model).
- Analyze the conversation text using OpenAI's GPT-3.5-turbo model.
- Provide sentiment and psychological insights for each speaker in the conversation, including their favorite and least favorite topics, personal profiles, and recommendations for future interactions.
- Assess the speakers' attitudes towards each other or any third person.

## Incremental Updates

### Explorer Mode
- Developed a web interface using Flask to allow users to upload conversation text files.
- Integrated with OpenAI's GPT-3.5-turbo API to analyze the conversation text and provide sentiment and psychological insights for each speaker.

### Adventure Mode
- Extended the web interface to allow users to upload audio files containing conversations.
- Integrated with the Deepgram API to transcribe the audio files and obtain the conversation text.
- Utilized the transcribed conversation text with OpenAI's API to generate insights, similar to the Explorer Mode.

### Master Mode
- Deployed the application on the Google Cloud Platform using Google Cloud Run with a Dockerized container for scalable processing.
- Developed a REST API endpoint (`/api`) to handle file uploads and analysis requests.
- The server URL for the deployed app is: https://dialogue-analyser-api-btkt3vr5aa-uc.a.run.app

### Grandmaster Mode
- Replaced the Deepgram API with the open-source WhisperX diarization/transcription model for improved performance and flexibility.
- Integrated with the Hugging Face Hub to download the required diarization pipeline for WhisperX.
- Utilized Hugging Face access tokens for authentication and downloading the diarization model.


## Usage

The following section provides the walkthrough of the web interface.

### Uploading Files Options: 
The main interface allows you to select the file type you want to analyze - either a Text File or an Audio File. If you choose Audio File (as shown in the second image), an additional option appears to select the API type for transcribing the audio, either Deepgram or WhisperX. Once you've made your selections, you can click the "Choose file" button to upload the respective file.



### Conversation Text Preview: 
After uploading the file, the application transcribes the audio (if an audio file was provided) or reads the text directly (if a text file was provided). The resulting conversation text is then displayed in the "Conversation Text Preview" section. This section provides a preview of the dialogue or conversation, with each speaker's utterances labeled.

### Insights: 
Upon successful analysis of the conversation text, the application generates sentiment and psychological insights for each speaker involved in the dialogue using  OpenAI's APIs. These insights are displayed in the "Insights" section, as depicted in the below image. The insights cover various aspects, such as the speakers' personalities, interests, attitudes towards each other, and recommendations for future interactions.


## Challenges Faced

### Research and API Integration
- Extensive research was required to identify suitable models and APIs for audio transcription, speaker diarization, and language analysis.
- Integrating various APIs and models into the application required understanding their documentation, handling authentication, and managing dependencies.
- Ensuring compatibility and seamless integration between different components was a challenge.

### Prompt Engineering
- Crafting the perfect prompt for OpenAI's GPT-3.5-turbo model to generate accurate and insightful analyses was a iterative process.
- Experimenting with different prompt structures, instruction formats, and example conversations was necessary to achieve satisfactory results.
- Fine-tuning the prompt to extract specific types of insights, such as sentiment analysis, psychological profiles, and speaker attitudes, required careful consideration.

### Performance and Scalability
- Deploying the application on the Google Cloud Platform with a containerized setup and leveraging the Cloud Run service ensured scalability and efficient resource allocation.
- Transcribing and analyzing audio files can be computationally expensive, especially for longer conversations or multiple speakers.
- Optimizing the performance of the application, including batching transcription requests and managing GPU memory, was crucial.

By addressing these challenges through research, experimentation, and iterative improvements, we were able to develop a robust and scalable application for dialogue analysis, capable of providing valuable insights into conversations.

## Instructions for Running the Code

### Local Development

1. Clone the repository: `git clone https://github.com/nmn-pandey/dialogue-analyser.git`
2. Install the required dependencies: `pip install -r requirements.txt`
3. Set the necessary API keys for OpenAI, Deepgram, and Hugging Face (if using WhisperX) in the `tokens.py` file.
4. Run the Flask app: `python app.py`
5. Access the web interface at `http://localhost:5001`

### Cloud Deployment (Google Cloud Run)

The application is deployed on Google Cloud Run with a REST API for scalable processing. The server URL is `https://dialogue-analyser-api-btkt3vr5aa-uc.a.run.app`.

To use the API, send a POST request to the `/api` endpoint with the following parameters:

- `file`: The text or audio file containing the conversation.
- `file_type`: Either `'text'` or `'audio'`.
- `api_type`: If `file_type` is `'audio'`, specify either `'deepgram'` or `'whisperx'` for the transcription API.

The API will return a JSON response containing the conversation text and the insights generated by the analysis.

## Contributions

Contributions to this project are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

Thank you for visiting.
