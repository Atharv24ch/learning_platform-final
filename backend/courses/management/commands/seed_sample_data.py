from django.core.management.base import BaseCommand
from courses.models import Roadmap, Lesson


class Command(BaseCommand):
    help = 'Seed a sample roadmap and lesson for local development'

    def handle(self, *args, **options):
        roadmap, _ = Roadmap.objects.get_or_create(
            topic='Sample AI Roadmap',
            defaults={
                'difficulty': 'Beginner',
                'content': {'sections': ['Intro', 'ML basics']},
                'duration_weeks': 4,
            },
        )

        # Ensure we have at least one lesson attached
        lesson_data = {
            'roadmap': roadmap,
            'title': 'Intro to AI',
            'content': 'Short description about AI basics.',
            'videos': [
                {
                    'video_id': 'abc123',
                    'title': 'AI Basics',
                    'description': 'Overview',
                    'thumbnail': 'https://i.ytimg.com/vi/abc123/default.jpg',
                    'embed_url': 'https://www.youtube.com/embed/abc123',
                }
            ],
            'order': 1,
        }

        lesson, created = Lesson.objects.get_or_create(
            roadmap=roadmap,
            title=lesson_data['title'],
            defaults={
                'content': lesson_data['content'],
                'videos': lesson_data['videos'],
                'order': lesson_data['order'],
            },
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Created lesson {lesson.id}'))
        else:
            self.stdout.write(self.style.WARNING(f'Lesson already exists (id={lesson.id})'))
