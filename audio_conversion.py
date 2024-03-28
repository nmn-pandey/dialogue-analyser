import whisperx
import gc 
from typing import Optional
import json
from huggingface_hub import hf_hub_download

from dotenv import load_dotenv

from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)

from tokens import DEEPGRAM_API_KEY, HUGGINGFACE_TOKEN

load_dotenv()

def deepgram_transcribe_and_annotate(
    audio_file: str
) -> str:
    try:
        # STEP 1 Create a Deepgram client using the API key
        deepgram = DeepgramClient(DEEPGRAM_API_KEY)

        with open(audio_file, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {
            "buffer": buffer_data,
        }

        #STEP 2: Configure Deepgram options for audio analysis
        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
            diarize=True,
            punctuate=True,
            utterances=True
        )

        # STEP 3: Call the transcribe_file method with the text payload and options
        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)

        transcription_file = response.to_json(indent=4)

        # # Specify the file path where you want to save the JSON data
        file_path = 'uploads/response.json'

        # # Write the JSON response to a file
        with open(file_path, 'w') as file:
            json.dump(response.to_json(indent=4), file)

        print("JSON response saved to:", file_path)

        # Parse JSON data
        data = json.loads(transcription_file)

        # Format the transcript to include speaker and utterance
        formatted_transcript = ""
        for utterance in data['results']['utterances']:
            speaker = f"Speaker {utterance['speaker']}:"
            transcript = utterance['transcript']
            formatted_transcript += f"{speaker} {transcript}\n\n"

        return formatted_transcript
    
    except Exception as e:
        print(f"Exception: {e}")




def whisperx_transcribe_and_annotate(
    audio_file: str,
    device: str = "cpu",
    batch_size: int = 4,
    compute_type: str = "int8",
    min_speakers: Optional[int] = 2,
    max_speakers: Optional[int] = 4,
) -> str:
    """
    Transcribe an audio file using WhisperX.

    Args:
        audio_file (str): Path to the audio file.
        device (str, optional): Device to use for model inference. Defaults to "cuda".
        batch_size (int, optional): Batch size for transcription. Defaults to 16.
        compute_type (str, optional): Compute type for the model. Defaults to "int8".
        hf_token (str, optional): Hugging Face token for downloading the diarization model. Defaults to None.
        min_speakers (int, optional): Minimum number of speakers in the audio. Defaults to None.
        max_speakers (int, optional): Maximum number of speakers in the audio. Defaults to None.

    Returns:
        str: A string containing the transcribed segments with speaker labels assigned.
    """
    # 1. Transcribe with original whisper (batched)
    model = whisperx.load_model("medium", device, compute_type=compute_type)
    audio = whisperx.load_audio(audio_file)
    result = model.transcribe(audio, batch_size=batch_size)

    # 2. Align whisper output
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

    # 3. Assign speaker labels
    diarize_model = whisperx.DiarizationPipeline(use_auth_token=HUGGINGFACE_TOKEN, device=device)
    diarize_segments = diarize_model(audio, min_speakers=min_speakers, max_speakers=max_speakers)
    result = whisperx.assign_word_speakers(diarize_segments, result)

    annotated_transcript = ""
    # Iterate over the segments and reconstruct the dialogue
    for segment in result["segments"]:
        speaker_id = segment['speaker']
        dialogue = ' '.join([word['word'] for word in segment['words']])
        print(f"Speaker {speaker_id}: {dialogue}")
        annotated_transcript += f"{speaker_id}: {dialogue}\n\n"

    # Clean up GPU memory
    gc.collect()
    del model, model_a, diarize_model

    return annotated_transcript

#result = whisperx_transcribe_and_annotate(audio_file = "uploads/audio.mp3", device = "cpu", batch_size=8)
#print(result)

#result = deepgram_transcribe_and_annotate(audio_file = "uploads/audio.mp3")
#print(result)

#diarize=true&punctuate=true&utterances=true