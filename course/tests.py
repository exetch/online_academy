import os
import sys
import django
sys.path.append('C:/Users/ASUS/PycharmProjects/online_academy')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from rest_framework.test import APITestCase
from users.models import CustomUser
from .models import Course, Subscription
from rest_framework import status

class CourseAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email='test@mail.com', password='12345')
        self.client.force_authenticate(user=self.user)

    def test_create_course_authenticated(self):
        data = {'title': 'New Course', 'description': 'New Description'}
        response = self.client.post('/courses/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)
        new_course = Course.objects.get(title=data['title'])
        self.assertEqual(new_course.description, data['description'])

    def test_create_course_unauthenticated(self):
        self.client.logout()
        data = {'title': 'New Course', 'description': 'New Description'}
        response = self.client.post('/courses/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_course_list(self):
        Course.objects.create(title="Course 1", description="Description 1", owner=self.user)
        Course.objects.create(title="Course 2", description="Description 2", owner=self.user)
        Course.objects.create(title="Course 3", description="Description 3", owner=self.user)
        response = self.client.get('/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

    def test_get_course_detail(self):
        course = Course.objects.create(title="Course 1", description="Description 1", owner=self.user)
        response = self.client.get(f'/courses/{course.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], course.title)
        self.assertEqual(response.data['description'], course.description)

    def test_update_course(self):
        course = Course.objects.create(title="Course 1", description="Description 1", owner=self.user)
        data = {'title': 'Updated Course', 'description': 'Updated Description'}
        response = self.client.put(f'/courses/{course.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_course = Course.objects.get(id=course.id)
        self.assertEqual(updated_course.title, data['title'])
        self.assertEqual(updated_course.description, data['description'])

    def test_delete_course(self):
        course = Course.objects.create(title="Course 1", description="Description 1", owner=self.user)
        response = self.client.delete(f'/courses/{course.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Course.objects.filter(id=course.id).exists())

    def test_subscribe_to_course(self):
        course = Course.objects.create(title="Course 1", description="Description 1", owner=self.user)
        response = self.client.post(f'/courses/{course.id}/subscribe/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        subscription = Subscription.objects.filter(user=self.user, course=course).first()
        self.assertIsNotNone(subscription)
        self.assertTrue(subscription.is_subscribed)

    def test_unsubscribe_from_course(self):
        course = Course.objects.create(title="Course 1", description="Description 1", owner=self.user)
        Subscription.objects.create(user=self.user, course=course, is_subscribed=True)
        response = self.client.post(f'/courses/{course.id}/unsubscribe/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        subscription = Subscription.objects.get(user=self.user, course=course)
        self.assertFalse(subscription.is_subscribed)