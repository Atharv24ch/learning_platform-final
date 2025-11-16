from django.db import models
from users.models import CustomUser

# quizzes/models.py
class Quiz(models.Model):
    lesson = models.ForeignKey('courses.Lesson', on_delete=models.CASCADE)
    questions = models.JSONField()  # Generated quiz questions
    created_at = models.DateTimeField(auto_now_add=True)
    
class QuizAttempt(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    answers = models.JSONField()
    results = models.JSONField()
    attempted_at = models.DateTimeField(auto_now_add=True)
