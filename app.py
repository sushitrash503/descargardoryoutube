from flask import Flask, request, jsonify, send_from_directory
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/get_video_info', methods=['POST'])
def get_video_info():
    url = request.json.get('url')
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', 'Unknown Title')
        video_uploader = info_dict.get('uploader', 'Unknown Uploader')
        thumbnail_url = info_dict.get('thumbnail', 'default_thumbnail_url')
        return jsonify({
            'title': video_title,
            'uploader': video_uploader,
            'thumbnail': thumbnail_url
        })

@app.route('/download', methods=['POST'])
def download():
    url = request.json.get('url')
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return jsonify({'message': 'Download complete'})

if __name__ == "__main__":
    app.run(debug=True)
