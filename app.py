from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/extract', methods=['POST'])
def extract_video():
    data = request.get_json()
    youtube_url = data.get('url')

    if not youtube_url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'quiet': True,
            'noplaylist': True
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            video_url = info.get('url', None)

        if video_url:
            return jsonify({'direct_link': video_url}), 200
        else:
            return jsonify({'error': 'Extraction failed'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
