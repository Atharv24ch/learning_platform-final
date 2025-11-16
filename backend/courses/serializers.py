from rest_framework import serializers
from .models import Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'roadmap', 'title', 'content', 'videos', 'order', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        # Ensure order has a sensible default (append to end)
        if 'order' not in validated_data or validated_data.get('order') is None:
            roadmap = validated_data.get('roadmap')
            if roadmap is not None:
                # compute next order for the roadmap
                last = Lesson.objects.filter(roadmap=roadmap).order_by('-order').first()
                validated_data['order'] = (last.order + 1) if last and last.order is not None else 1
            else:
                validated_data['order'] = 1

        return super().create(validated_data)
