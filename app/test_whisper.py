from app.services.transcription.whisper_service import transcribe_audio

result = transcribe_audio("adjectives1-1.mp3")

print(result)