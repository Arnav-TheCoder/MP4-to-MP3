from flask import Flask, render_template_string, request, send_file
from moviepy import VideoFileClip
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>MP4 to MP3 Converter</title>
</head>
<body style="font-family: Arial; margin: 40px;">
    <h2>Upload an MP4 file to convert it to MP3</h2>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="video" accept=".mp4" required>
        <button type="submit">Convert</button>
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def upload_and_convert():
    if request.method == "POST":
        uploaded = request.files["video"]

        if uploaded.filename == "":
            return "No file selected."

        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Save uploaded MP4
        mp4_path = os.path.join(script_dir, uploaded.filename)
        uploaded.save(mp4_path)

        base = os.path.splitext(uploaded.filename)[0]
        mp3_path = os.path.join(script_dir, base + ".mp3")

        # Convert to MP3
        video = VideoFileClip(mp4_path)
        audio = video.audio
        audio.write_audiofile(mp3_path)
        audio.close()
        video.close()

        return send_file(mp3_path, as_attachment=True)

    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(debug=True)
