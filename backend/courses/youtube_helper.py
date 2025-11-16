from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Lesson

# Load environment variables
load_dotenv()

def search_youtube_videos(query, max_results=5):
    """
    Search YouTube for educational videos
    """
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        # Fallback to hardcoded key if env not set
        api_key = 'AIzaSyAxaVRY79ZFLaksu66pfNEqX-C5kZXXF8U'
    
    youtube = build(
        'youtube', 
        'v3', 
        developerKey=api_key
    )
    
    search_response = youtube.search().list(
        q=query,
        part='id,snippet',
        maxResults=max_results,
        type='video',
        videoCaption='closedCaption',  # Only videos with captions
        order='relevance'
    ).execute()
    
    videos = []
    for item in search_response.get('items', []):
        if item['id']['kind'] == 'youtube#video':
            videos.append({
                'video_id': item['id']['videoId'],
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'thumbnail': item['snippet']['thumbnails']['high']['url'],
                'channel': item['snippet']['channelTitle'],
                'embed_url': f"https://www.youtube.com/embed/{item['id']['videoId']}"
            })
    
    return videos

class LessonView(APIView):
    def post(self, request):
        lesson_topic = request.data.get('topic')
        
        # Search for relevant videos
        videos = search_youtube_videos(
            f"{lesson_topic} tutorial",
            max_results=3
        )
        
        # Create lesson with videos
        lesson = Lesson.objects.create(
            roadmap_id=request.data.get('roadmap_id'),
            title=lesson_topic,
            videos=videos,
            content=request.data.get('content', '')
        )
        
        return Response({
            'lesson_id': lesson.id,
            'videos': videos
        }, status=status.HTTP_201_CREATED)

len