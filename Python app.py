from flask import Flask, request, jsonify
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import os
from moviepy.editor import VideoFileClip

app = Flask(__YOUTUBE__)

DEVELOPER_KEY = AIzaSyCQ0j6RSbM-wjw-PpLCaEd2u9R0h63CrfE
YOUTUBE_UPLOAD_URL = 'https://www.googleapis.com/upload/youtube/v3/videos'

def youtube_upload(filename, title, description, keywords, privacyStatus):
    youtube = build('youtube', 'v3', developerKey=AIzaSyCQ0j6RSbM
    media_file = MediaFileUpload(filename, mimetype='video/mp4', chunksize=-1, resumable=True)

    request = youtube.videos().insert(
        part='snippet,status',
        body={
            'snippet': {
                'title': title,
                'description': description,
                'tags': keywords,
            },
            'status': {
                'privacyStatus': privacyStatus
            }
        },
        media_body=media_file
    )

    response = None
    try:
        response = request.execute()
    except HttpError as e:
        print(f'An HTTP error occurred: {e}')
        # Manejo del error

    if response:
        print(f'Video uploaded successfully! Video ID: {response["id"]}')
        # Manejo del éxito

def extract_metadata(filename):
    try:
        clip = VideoFileClip(filename)
        title = os.path.splitext(os.path.basename(filename))[0]
        description = "Descripción automática del video"
        keywords = ["palabras clave", "keywords"]
        return title, description, keywords
    except Exception as e:
        print(f'Error al extraer metadatos: {e}')
        return None, None, None

@app.route('/upload', methods=['POST'])
def upload_video():
    filename = request.form.get('filename')
    title = request.form.get('title')
    description = request.form.get('description')
    keywords = request.form.get('keywords')
    privacyStatus = request.form.get('privacyStatus')

    youtube_upload(filename, title, description, keywords, privacyStatus)

    return jsonify({'message': 'Video uploaded successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
