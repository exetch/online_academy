from django.db import models
from course.models import Course


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')
    title = models.CharField(max_length=200, verbose_name='Название')
    preview = models.ImageField(upload_to='lesson_previews/', verbose_name='Превью')
    description = models.TextField(verbose_name='Описание')
    video_url = models.URLField(verbose_name='Ссылка на видео')

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title
