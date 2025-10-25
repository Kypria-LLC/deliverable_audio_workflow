import requests
import shutil
import subprocess
import os
import time

# YouTube-specific imports
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload

# Prerequisites: pip install requests google-api-python-client google-auth-httplib2 google-auth-oauthlib yt-dlp
# Also, install ffmpeg (e.g., via apt install ffmpeg or brew install ffmpeg)
# For YouTube: Download client_secrets.json from Google Developers Console

# Replace these:
access_token = 'YOUR_PAGE_ACCESS_TOKEN'
page_id = 'YOUR_PAGE_ID'
instagram_account_id = 'YOUR_INSTAGRAM_ACCOUNT_ID'
audio_file_path = 'zeus-invocation.mp3'
placeholder_image = 'placeholder.jpg'  # Static image for video overlay
video_file_path = 'output.mp4'
audio_caption = 'ZEUS Invocation Audio'
public_video_url = 'https://your-domain.com/output.mp4'  # Must be publicly accessible
extracted_audio_path = 'extracted-zeus-invocation.mp3'

# YouTube settings
CLIENT_SECRETS_FILE = 'client_secrets.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
youtube_title = audio_caption
youtube_description = 'Audio converted to video for playback.'
youtube_category_id = '22'  # People & Blogs
youtube_keywords = 'audio,invocation,zeus'
youtube_privacy_status = 'private'  # 'public', 'private', or 'unlisted'

# Function to get authenticated YouTube service
def get_authenticated_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)

# Optional: Convert audio to video using ffmpeg
if not os.path.exists(video_file_path):
    try:
        subprocess.run([
            'ffmpeg', '-loop', '1', '-i', placeholder_image, '-i', audio_file_path,
            '-shortest', '-c:v', 'libx264', '-c:a', 'aac', '-b:a', '192k', video_file_path
        ], check=True)
        print("Converted audio to video:", video_file_path)
    except subprocess.CalledProcessError as e:
        print("FFmpeg conversion failed:", e)
        exit(1)

# Step 1: Upload video to Facebook page
url_fb = f"https://graph.facebook.com/v21.0/{page_id}/videos"
files = {
    'source': open(video_file_path, 'rb'),
}
data = {
    'access_token': access_token,
    'title': audio_caption,
    'description': 'Audio converted to video for playback.',
}
response_fb = requests.post(url_fb, files=files, data=data)
fb_data = response_fb.json()
print("Facebook upload response:", fb_data)
fb_video_id = fb_data.get('id')

# Step 2: Upload and publish Reel to Instagram
# Create media container
url_ig_media = f"https://graph.facebook.com/v21.0/{instagram_account_id}/media"
params_ig = {
    'media_type': 'REELS',
    'video_url': public_video_url,
    'caption': f'{audio_caption} as Reel',
    'access_token': access_token,
}
response_media = requests.post(url_ig_media, data=params_ig)
media_data = response_media.json()
print("Instagram media creation response:", media_data)

if 'id' in media_data:
    container_id = media_data['id']
    
    # Check container status
    url_status = f"https://graph.facebook.com/v21.0/{container_id}?fields=status_code&access_token={access_token}"
    status = 'IN_PROGRESS'
    while status != 'FINISHED':
        response_status = requests.get(url_status)
        status_data = response_status.json()
        status = status_data.get('status_code', 'UNKNOWN')
        print(f"Container status: {status}")
        if status == 'ERROR':
            print("Error in container:", status_data)
            break
        time.sleep(5)  # Wait 5 seconds before checking again
    
    if status == 'FINISHED':
        # Publish the Reel
        url_publish = f"https://graph.facebook.com/v21.0/{instagram_account_id}/media_publish"
        params_publish = {
            'creation_id': container_id,
            'access_token': access_token,
        }
        response_publish = requests.post(url_publish, data=params_publish)
        publish_data = response_publish.json()
        print("Instagram publish response:", publish_data)
        
        if 'id' in publish_data:
            ig_media_id = publish_data['id']
            
            # Get direct media URL
            url_media = f"https://graph.facebook.com/v21.0/{ig_media_id}?fields=media_url&access_token={access_token}"
            response_media_url = requests.get(url_media)
            media_info = response_media_url.json()
            direct_video_url = media_info.get('media_url')
            print("Instagram Media Direct URL:", direct_video_url)
            
            # Optional: Extract audio from video using ffmpeg
            if direct_video_url:
                try:
                    # Download the video first
                    with requests.get(direct_video_url, stream=True) as r, open("temp_video.mp4", "wb") as f:
                        shutil.copyfileobj(r.raw, f)
                    # Extract audio
                    subprocess.run([
                        'ffmpeg', '-i', 'temp_video.mp4', '-vn', '-acodec', 'libmp3lame', extracted_audio_path
                    ], check=True)
                    print("Extracted audio from video:", extracted_audio_path)
                    os.remove("temp_video.mp4")  # Clean up
                except subprocess.CalledProcessError as e:
                    print("FFmpeg extraction failed:", e)
            
            # Step 3: Upload video to YouTube
            try:
                youtube = get_authenticated_service()
                body = {
                    'snippet': {
                        'title': youtube_title,
                        'description': youtube_description,
                        'tags': youtube_keywords.split(','),
                        'categoryId': youtube_category_id
                    },
                    'status': {
                        'privacyStatus': youtube_privacy_status
                    }
                }
                media = MediaFileUpload(video_file_path, resumable=True)
                request = youtube.videos().insert(
                    part='snippet,status',
                    body=body,
                    media_body=media
                )
                response = request.execute()
                youtube_video_id = response['id']
                print(f"YouTube upload successful! Video ID: {youtube_video_id}")
                youtube_url = f"https://youtube.com/watch?v={youtube_video_id}"
                
                # Step 4: Download audio from YouTube using yt-dlp
                try:
                    subprocess.run([
                        'yt-dlp', '-f', 'bestaudio', '-o', 'zeus-invocation.%(ext)s', youtube_url
                    ], check=True)
                    print("Downloaded audio from YouTube as zeus-invocation.mp3 (or similar)")
                except subprocess.CalledProcessError as e:
                    print("yt-dlp download failed:", e)
            except Exception as e:
                print("YouTube upload failed:", e)
            
            # Deliverable: Provide downloadable URLs
            print("\n🎯 Deliverable URLs:")
            if fb_video_id:
                print(f"Facebook Video URL: https://www.facebook.com/{page_id}/videos/{fb_video_id}")
            if direct_video_url:
                print(f"Instagram Media URL: {direct_video_url}")
            if youtube_video_id:
                print(f"YouTube Video URL: {youtube_url}")
            print("Use the downloaded zeus-invocation.mp3 file for attachment to your site, portal, or asset library.")
else:
    print("Instagram media creation failed:", media_data)
