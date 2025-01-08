import speech_recognition as sr
from pydub import AudioSegment

# Convert .m4a to .wav
def convert_audio_to_wav(input_path, output_path):
    try:
        print("Converting .m4a to .wav...")
        audio = AudioSegment.from_file(input_path, format="m4a")
        audio.export(output_path, format="wav")
        print("Conversion complete.")
    except Exception as e:
        print(f"Error converting audio: {e}")
        raise

# Save transcription to a text file
def save_transcription_to_file(transcription, output_file_path):
    try:
        with open(output_file_path, "w") as file:
            file.write(transcription)
        print(f"Transcription saved to {output_file_path}")
    except Exception as e:
        print(f"Error saving transcription: {e}")
        raise

# Paths
input_audio_path = "Conflict in project.m4a"
output_audio_path = "Conflict_in_project.wav"
output_transcription_path = "transcription.txt"

# Convert to .wav
convert_audio_to_wav(input_audio_path, output_audio_path)

# Initialize recognizer
recognizer = sr.Recognizer()

# Transcribe the .wav file
try:
    with sr.AudioFile(output_audio_path) as source:
        print("Loading audio...")
        audio_data = recognizer.record(source)
    
    print("Transcribing audio...")
    transcription = recognizer.recognize_google(audio_data)
    print("\nTranscription:")
    print(transcription)
    
    # Save transcription to file
    save_transcription_to_file(transcription, output_transcription_path)

except sr.UnknownValueError:
    print("Sorry, the audio was not clear enough to transcribe.")
except sr.RequestError as e:
    print(f"Could not request results from the recognition service; {e}")

