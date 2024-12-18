from datetime import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from callboard.models import Ad, Feedback
from users.models import User


class AdTestCase(APITestCase):
    """Класс для проверки корректности работы CRUD объявлений"""

    def setUp(self):
        self.user = User.objects.create(email='test@example.ru')
        self.user.set_password('test')
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.ad = Ad.objects.create(
            title='Тестовое объявление №1',
            price=500,
            description='Тестовое описание объявления №1',
            author=self.user,
            created_at='2024-12-18T13:00:00Z',
        )

    def test_create_ad(self):
        """Создание объявления"""
        url = reverse('callboard:ad_create')
        data = {
            'title': 'Тестовое объявление №2',
            'price': 600,
            'description': 'Тестовое описание объявления №2',
            'author': self.user.pk,
            'created_at' : '2024-12-18T13:00:00Z',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ad.objects.count(), 2)
        self.assertTrue(Ad.objects.all().exists())

    def test_ads_list(self):
        """Вывод списка объявлений"""
        url = reverse('callboard:ad_list')
        response = self.client.get(url)
        data = response.json()
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.ad.pk,
                    'title': 'Тестовое объявление №1',
                    'price': 500,
                    'description': 'Тестовое описание объявления №1',
                    'created_at': datetime.isoformat(self.ad.created_at),
                    'author': self.user.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_ad_retrieve(self):
        """Проверка корректности данных"""
        url = reverse('callboard:ad_retrieve', args=(self.ad.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['title'], self.ad.title)
        self.assertEqual(data['price'], self.ad.price)
        self.assertEqual(data['description'], self.ad.description)
        self.assertEqual(data['created_at'], datetime.isoformat(self.ad.created_at))
        self.assertEqual(data['author'], self.user.pk)

    def test_ad_update(self):
        """Проверка обновления объявления"""
        url = reverse('callboard:ad_update', args=(self.ad.pk,))
        data = {
            'title': 'Тестовое объявление №1 обновлено',
            'description': 'Тестовое описание объявления №1 обновлено',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['title'], 'Тестовое объявление №1 обновлено')
        self.assertEqual(
            data['description'], 'Тестовое описание объявления №1 обновлено'
        )

    def test_ad_delete(self):
        """Проверка удаления объявления"""
        url = reverse('callboard:ad_delete', args=(self.ad.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ad.objects.count(), 0)


class FeedbackTestCase(APITestCase):
    """Класс для проверки корректности работы CRUD объявлений"""

    def setUp(self):
        self.user = User.objects.create(email='test@example.ru')
        self.user.set_password('test')
        self.user.save()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.ad = Ad.objects.create(
            title='Тестовое объявление №1',
            price=500,
            description='Тестовое описание объявления №1',
            author=self.user,
        )
        self.feedback = Feedback.objects.create(
            text='Отзыв на тестовое объявление №1',
            author=self.user,
            ad=self.ad,
        )

    def test_create_feedback(self):
        """Создание отзыва"""
        url = f'/callboard/{self.ad.pk}/feedbacks/create/'
        data = {
            'text': 'Новый отзыв на тестовое объявление №1',
            'author': self.user.pk,
            'ad': self.ad.pk,
            'created_at': '2024-12-17T16:00:00Z',
        }
        response = self.client.post(url, data, format='json')
        author = self.user
        feedback = Feedback.objects.get(text='Новый отзыв на тестовое объявление №1')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Feedback.objects.count(), 2)
        self.assertTrue(author, feedback.author)

    def test_feedback_list(self):
        """Вывод списка отзывов на объявление"""
        url = f'/callboard/{self.ad.pk}/feedbacks/'
        response = self.client.get(url)
        data = response.json()
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.feedback.pk,
                    'text': 'Отзыв на тестовое объявление №1',
                    'created_at': datetime.isoformat(self.feedback.created_at),
                    'author': self.user.pk,
                    'ad': self.ad.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Feedback.objects.count(), 1)
        self.assertEqual(data, result)

    def test_feedback_retrieve(self):
        """Проверка корректности данных"""
        url = f'/callboard/feedbacks/{self.feedback.pk}/'
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['text'], self.feedback.text)
        self.assertEqual(data['author'], self.user.pk)
        self.assertEqual(data['ad'], self.ad.pk)
        self.assertEqual(
            data['created_at'], datetime.isoformat(self.feedback.created_at)
        )

    def test_feedback_update(self):
        """Проверка обновления отзыва"""
        url = f'/callboard/feedbacks/{self.feedback.pk}/update/'
        data = {
            'text': 'Отзыв объявления №1 обновлен',
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['text'], 'Отзыв объявления №1 обновлен')

    def test_feedback_delete(self):
        """Проверка удаления отзыва"""
        url = f'/callboard/feedbacks/{self.feedback.pk}/delete/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ad.objects.count(), 1)
