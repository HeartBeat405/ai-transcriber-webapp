import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import assemblyai as aai

# Load .env
load_dotenv()

# Flask App
app = Flask(__name__)

# Upload Folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# AssemblyAI API Key
aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# Transcribe Route
@app.route("/transcribe", methods=["POST"])
def transcribe_audio():

    # Check file
    if "audio" not in request.files:
        return jsonify({
            "success": False,
            "error": "No file uploaded"
        }), 400

    file = request.files["audio"]

    # Empty file
    if file.filename == "":
        return jsonify({
            "success": False,
            "error": "No selected file"
        }), 400

    # Save file
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    file.save(filepath)

    try:

        # CONFIG FINAL TERBARU
        config = aai.TranscriptionConfig(
            speech_models=[
                "universal-3-pro",
                "universal-2"
            ]
        )

        # Create Transcriber
        transcriber = aai.Transcriber(config=config)

        # Transcribe
        transcript = transcriber.transcribe(filepath)

        # Success
        return jsonify({
            "success": True,
            "text": transcript.text
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# Run Flask
if __name__ == "__main__":
    app.run(debug=True)