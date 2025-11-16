# courses/models.py
from django.db import models
from users.models import CustomUser

class Roadmap(models.Model):
    # Make user optional so anonymous or system-generated roadmaps can be created
    # without violating DB constraints. This was changed to avoid errors when
    # generating fallback roadmaps on development/live servers where the
    # requester may not be authenticated.
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    topic = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=50)
    content = models.JSONField()  # Structured roadmap data
    duration_weeks = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class Lesson(models.Model):
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    videos = models.JSONField(default=list)  # YouTube video data
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


