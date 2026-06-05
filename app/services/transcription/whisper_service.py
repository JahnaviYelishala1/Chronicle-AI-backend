from faster_whisper import WhisperModel

model = None


def get_model():
    global model

    if model is None:
        model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8"
        )

    return model

def transcribe_audio(audio_path: str):

    segments, info = get_model().transcribe(
        audio_path
    )

    transcript = ""

    for segment in segments:
        transcript += segment.text + " "

    return transcript.strip()
