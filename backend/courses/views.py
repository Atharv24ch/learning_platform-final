from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from asgiref.sync import async_to_sync

from .ai_helpers import generate_learning_roadmap  # async function
from .youtube_helper import search_youtube_videos
from .models import Lesson, Roadmap
from .serializers import LessonSerializer



class GenerateRoadmapView(APIView):
    def post(self, request):
        """Create a learning roadmap.

        This is a synchronous DRF view that calls an async generator.
        We use asgiref.sync.async_to_sync so this works under both WSGI
        and ASGI servers without creating a new event loop.
        """
        topic = request.data.get("topic")
        difficulty_level = request.data.get("difficulty")
        duration_weeks = request.data.get("duration_weeks")

        if not topic or not difficulty_level or duration_weeks is None:
            return Response(
                {"detail": "topic, difficulty, duration_weeks are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate and coerce duration_weeks to int
        try:
            duration_weeks = int(duration_weeks)
            if duration_weeks <= 0:
                raise ValueError("duration_weeks must be a positive integer")
        except Exception as e:
            return Response({"detail": f"Invalid duration_weeks: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Run the async function in a compatible way
            roadmap_data = async_to_sync(generate_learning_roadmap)(topic, difficulty_level, duration_weeks)
        except Exception as e:
            return Response(
                {"detail": f"Error generating roadmap: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Save the roadmap to database
        try:
            # Get the current user if authenticated, otherwise None
            user = request.user if request.user.is_authenticated else None
            
            # Create the roadmap in the database
            roadmap_obj = Roadmap.objects.create(
                user=user,
                topic=topic,
                difficulty=difficulty_level,
                content=roadmap_data,  # Store the entire generated structure
                duration_weeks=duration_weeks
            )
            
            # Create lessons from the weeks in the roadmap
            weeks = roadmap_data.get('weeks', [])
            for idx, week_content in enumerate(weeks, start=1):
                # Extract a search query from the week content for YouTube videos
                # Use the first 50 chars of week content + topic as search query
                search_query = f"{topic} {week_content[:50]}"
                
                # Fetch related YouTube videos
                try:
                    videos = search_youtube_videos(search_query, max_results=3)
                except Exception as e:
                    print(f"Error fetching videos for week {idx}: {e}")
                    videos = []
                
                Lesson.objects.create(
                    roadmap=roadmap_obj,
                    title=f"Week {idx}",
                    content=week_content,
                    videos=videos,
                    order=idx
                )
            
            # Return the roadmap data with the database ID
            response_data = {
                'id': roadmap_obj.id,
                **roadmap_data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {"detail": f"Error saving roadmap: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class YouTubeSearchView(APIView):
    """Search YouTube for videos using the helper function.

    GET params:
      - q or query: search query (required)
      - max_results: optional int, default 5
    """
    def get(self, request):
        q = request.query_params.get('q') or request.query_params.get('query')
        if not q:
            return Response({'detail': 'query (q) parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

        max_results = request.query_params.get('max_results', 5)
        try:
            max_results = int(max_results)
            if max_results <= 0:
                raise ValueError()
        except Exception:
            return Response({'detail': 'max_results must be a positive integer.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            videos = search_youtube_videos(q, max_results=max_results)
        except Exception as e:
            return Response({'detail': f'Error searching YouTube: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'videos': videos}, status=status.HTTP_200_OK)


class LessonListCreateView(generics.ListCreateAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        qs = Lesson.objects.all().order_by('order', 'id')
        roadmap_id = self.request.query_params.get('roadmap')
        if roadmap_id:
            try:
                roadmap_id = int(roadmap_id)
                qs = qs.filter(roadmap_id=roadmap_id)
            except ValueError:
                qs = qs.none()
        return qs

    def perform_create(self, serializer):
        # serializer.create will handle default order if not provided
        serializer.save()


class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    

