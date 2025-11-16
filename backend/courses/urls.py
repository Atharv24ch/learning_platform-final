from django.urls import path
from .views import GenerateRoadmapView, YouTubeSearchView, LessonListCreateView, LessonDetailView

urlpatterns = [
    path('generate/', GenerateRoadmapView.as_view(), name='generate-roadmap'),
    path('youtube/search/', YouTubeSearchView.as_view(), name='youtube-search'),

    # Lessons CRUD
    path('lessons/', LessonListCreateView.as_view(), name='lessons-list-create'),
    path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lessons-detail'),
]
