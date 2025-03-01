from flask import Flask, request, Response, send_from_directory
from speech_processor import transcribe_audio, generate_voice_response
from twilio.twiml.voice_response import VoiceResponse
import requests
import os

app = Flask(__name__)



# Set Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CREDENTIALS

# Serve static audio files from the audio_prompts directory
@app.route('/audio/<path:filename>')
def serve_audio(filename):
    return send_from_directory('audio_prompts', filename)

@app.route("/call", methods=["POST"])
def handle_call():
    response = VoiceResponse()
    response.play("https://quanvance.com/audio/Welcome (General).wav")
    response.record(action="/process_recording", max_length=10)
    return Response(str(response), mimetype="text/xml")

@app.route("/process_recording", methods=["POST"])
def process_recording():
    recording_url = request.values.get("RecordingUrl")
    if recording_url:
        # Download the Twilio recording
        response = requests.get(recording_url)
        with open("temp.wav", "wb") as f:
            f.write(response.content)
        # Transcribe the audio
        transcript = transcribe_audio("temp.wav")
        parts = transcript.split(",")
        if len(parts) >= 3:
            name, skill, availability = [p.strip() for p in parts[:3]]
            from profile_manager import store_worker_profile
            store_worker_profile(name, skill, availability)
            # Generate dynamic response in Hindi
            response_text = f"ठीक है, {name}। आप {skill} के रूप में पंजीकृत हो गए हैं, उपलब्ध {availability}।"
            audio_file = generate_voice_response(response_text, "audio_prompts/temp_response.wav")
            response = VoiceResponse()
            response.play("https://quanvance.com/audio/temp_response.wav")
            return Response(str(response), mimetype="text/xml")
        else:
            response = VoiceResponse()
            response.play("https://quanvance.com/audio/Unclear Input.wav")
            response.record(action="/process_recording", max_length=10)
            return Response(str(response), mimetype="text/xml")
    response = VoiceResponse()
    response.play("https://quanvance.com/audio/Unclear Input.wav")
    return Response(str(response), mimetype="text/xml")

if __name__ == "__main__":
    app.run(debug=True, port=5000)