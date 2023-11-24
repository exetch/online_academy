import re
from rest_framework import serializers
from .models import Lesson

class YouTubeURLValidator:
    def __init__(self, field):
        self.field = field
    def __call__(self, value):
        tmp_value = dict(value).get(self.field)
        if tmp_value is not None:
            pattern = r'^https?://(www\.)?youtube\.com/watch\?v=[\w-]+$'
            if not re.match(pattern, tmp_value):
                raise serializers.ValidationError("Корректны ссылки только с ресурса youtube.com.")

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [YouTubeURLValidator(field='video_url')]
