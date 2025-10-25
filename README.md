# Deliverable Audio Workflow

Automated workflow for uploading audio/video content to Meta (Facebook/Instagram) and YouTube. Converts audio to video, manages uploads, extracts media, and provides deliverable URLs for invocation delivery.

## Overview

This Python script provides a comprehensive automation workflow for:
- Converting audio files to video format with placeholder images
- Uploading videos to Facebook pages
- Publishing Reels to Instagram
- Uploading videos to YouTube
- Extracting and downloading audio from published videos
- Retrieving direct media URLs for all platforms

## Features

- **Audio to Video Conversion**: Uses FFmpeg to convert audio files (MP3) to video format with a static placeholder image
- **Multi-Platform Upload**: Automates uploads to Facebook, Instagram (Reels), and YouTube
- **Media Extraction**: Downloads audio from YouTube videos using yt-dlp
- **Direct URL Retrieval**: Provides accessible URLs for all uploaded content
- **Status Monitoring**: Tracks upload and processing status across platforms

## Prerequisites

### Python Packages
```bash
pip install requests google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### External Tools
- **FFmpeg**: For audio/video conversion
  - Ubuntu/Debian: `apt install ffmpeg`
  - macOS: `brew install ffmpeg`
- **yt-dlp**: For YouTube audio downloads
  - Install via pip: `pip install yt-dlp`

### API Credentials

1. **Facebook/Instagram**:
   - Facebook Page Access Token
   - Facebook Page ID
   - Instagram Business Account ID
   - Set up via [Facebook Developers Console](https://developers.facebook.com/)

2. **YouTube**:
   - Google API Client Secrets JSON file (`client_secrets.json`)
   - Download from [Google Developers Console](https://console.developers.google.com/)

## Configuration

Update the following variables in the script:

```python
access_token = 'YOUR_PAGE_ACCESS_TOKEN'
page_id = 'YOUR_PAGE_ID'
instagram_account_id = 'YOUR_INSTAGRAM_ACCOUNT_ID'
audio_file_path = 'zeus-invocation.mp3'
placeholder_image = 'placeholder.jpg'
public_video_url = 'https://your-domain.com/output.mp4'  # Must be publicly accessible
```

## Workflow Steps

1. **Convert Audio to Video**: Combines audio file with a static image to create a video
2. **Upload to Facebook**: Posts video to specified Facebook page
3. **Publish Instagram Reel**: Creates and publishes a Reel to Instagram
4. **Upload to YouTube**: Authenticates and uploads video to YouTube
5. **Extract Audio**: Downloads audio from the YouTube video
6. **Provide Deliverables**: Outputs URLs for all platforms

## Usage

```bash
python deliverable_audio_workflow.py
```

## Output

The script provides:
- Facebook video URL
- Instagram media direct URL
- YouTube video URL
- Downloaded audio file (MP3)

## Use Cases

- **Invocation Delivery**: Automated distribution of spiritual invocations and audio content
- **Content Syndication**: Multi-platform publishing for audio content creators
- **Media Archival**: Automated backup and retrieval of audio content
- **Social Media Automation**: Streamlined posting to multiple social platforms

## License

This project is provided for automation purposes related to Meta/Instagram/YouTube audio/video content delivery.

## Author

KYPRIA LLC
