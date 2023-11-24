import os
import sys
import django
sys.path.append('C:/Users/ASUS/PycharmProjects/online_academy')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from rest_framework.test import APITestCase
from users.models import CustomUser
from .models import Course, Lesson
from rest_framework import status

class LessonAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email='test@mail.com', password='12345')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="Test Course", description="Test Description", owner=self.user)

    def test_create_lesson(self):
        data = {
            'course': self.course.id,
            'title': 'New Lesson',
            'description': 'Lesson Description',
            'video_url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        }
        response = self.client.post('/lessons/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)
        new_lesson = Lesson.objects.get(title=data['title'])
        self.assertEqual(new_lesson.description, data['description'])
        self.assertEqual(new_lesson.video_url, data['video_url'])

    def test_retrieve_lesson(self):
        lesson = Lesson.objects.create(course=self.course, title="Lesson 1", description="Description",
                                       video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", owner=self.user)
        response = self.client.get(f'/lessons/{lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], lesson.title)
        self.assertEqual(response.data['description'], lesson.description)
        self.assertEqual(response.data['video_url'], lesson.video_url)

    def test_update_lesson(self):
        lesson = Lesson.objects.create(course=self.course, title="Lesson 1", description="Description", video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", owner=self.user)
        update_data = {'title': 'Updated Lesson', 'description': 'New Description', 'course': self.course.id}
        response = self.client.put(f'/lessons/{lesson.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_lesson = Lesson.objects.get(id=lesson.id)
        self.assertEqual(updated_lesson.title, update_data['title'])

    def test_delete_lesson(self):
        lesson = Lesson.objects.create(course=self.course, title="Lesson 1", description="Description", video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", owner=self.user)
        response = self.client.delete(f'/lessons/{lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_get_lesson_list(self):
        Lesson.objects.create(course=self.course, title='Lesson 1', description='Description 1', owner=self.user)
        Lesson.objects.create(course=self.course, title='Lesson 2', description='Description 2', owner=self.user)
        response = self.client.get('/lessons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['title'], 'Lesson 1')
        self.assertEqual(response.data['results'][1]['title'], 'Lesson 2')

    def test_lesson_with_invalid_url(self):
        invalid_youtube_url = "https://invalidurl.com/watch?v=dQw4w9WgXcQ"

        lesson_data = {
            'course': self.course.id,
            'title': 'Test Lesson',
            'description': 'Test Description',
            'video_url': invalid_youtube_url,
            'owner': self.user.id
        }
        response = self.client.post('/lessons/', lesson_data)
        self.assertEqual(response.json()['non_field_errors'][0], "Корректны ссылки только с ресурса youtube.com.")