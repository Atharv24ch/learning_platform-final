from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    learning_preferences = models.JSONField(default=dict, blank=True)
    
class UserProgress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    roadmap = models.ForeignKey('courses.Roadmap', on_delete=models.CASCADE)
    completed_lessons = models.JSONField(default=list)
    quiz_scores = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
