import json
# from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Passage, User, Coords, Level, Images
from .serializers import PassageSerializer


# Create your tests here.
# Тест для проверки функционала нашего Passage REST-API
class PassageTest(APITestCase):
    # создаем данные, с которыми будем работать в последующих тестах
    def setUp(self):
        # два объекта перевалов:
        # первый перевал
        self.passage1 = Passage.objects.create(
            beauty_title='перевал',
            title='Перевал1',
            other_titles='',
            connect='',
            user=User.objects.create(
                email='email1@gmail.com',
                fam='Фамилия1',
                name='Имя1',
                otc='Отчество1',
                phone='89271001010'
            ),
            coords=Coords.objects.create(
                latitude=11.1,
                longitude=11.1,
                height=1111
            ),
            level=Level.objects.create(
                winter='',
                summer='1a',
                autumn='1a',
                spring=''
            )
        )
        # картинки к первому перевалу
        self.image11 = Images.objects.create(
            data='http://www.passages.com/passage11.jpg',
            title='Перевал-1-1',
            passage=self.passage1
        )
        self.image12 = Images.objects.create(
            data='http://www.passages.com/passage12.jpg',
            title='Перевал-1-2',
            passage=self.passage1
        )
        self.image13 = Images.objects.create(
            data='http://www.passages.com/passage13.jpg',
            title='Перевал-1-3',
            passage=self.passage1
        )

        # второй перевал
        self.passage2 = Passage.objects.create(
            beauty_title='перевал',
            title='Перевал2',
            other_titles='',
            connect='',
            user=User.objects.create(
                email='email2@gmail.com',
                fam='Фамилия2',
                name='Имя2',
                otc='',
                phone='89272002020'
            ),
            coords=Coords.objects.create(
                latitude=22.2,
                longitude=22.2,
                height=2222
            ),
            level=Level.objects.create(
                winter='',
                summer='1b',
                autumn='1b',
                spring=''
            ),
            status='pending'
        )
        # картинки ко второму перевалу
        self.image21 = Images.objects.create(
            data='http://www.passages.com/passage21.jpg',
            title='Перевал-2-1',
            passage=self.passage2
        )
        self.image22 = Images.objects.create(
            data='http://www.passages.com/passage22.jpg',
            title='Перевал-2-2',
            passage=self.passage2
        )
        self.image23 = Images.objects.create(
            data='http://www.passages.com/passage23.jpg',
            title='Перевал-2-3',
            passage=self.passage2
        )

    # проверяем получение всех записей о перевалах
    def test_passages_list(self):
        response = self.client.get(reverse('passage-list'))
        serializer_data = PassageSerializer([self.passage1, self.passage2], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 2)
        self.assertEqual(serializer_data, response.data.get('results'))

    # проверяем получение записи о втором перевале
    def test_passage_detail(self):
        response = self.client.get(reverse('passage-detail', kwargs={'pk': self.passage2.id}))
        serializer_data = PassageSerializer(self.passage2).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    # проверяем создание записи о перевале и использование данных пользователя, если он уже есть в БД, вместо создания
    # нового
    def test_valid_create_and_user_reuse(self):
        data = {
            'beauty_title': 'перевал',
            'title': 'Перевал3',
            'other_titles': '',
            'connect': '',
            'user': {
                'email': 'email1@gmail.com',
                'fam': 'Фамилия1',
                'name': 'Имя1',
                'otc': 'Отчество1',
                'phone': '89271001010'
            },
            'coords': {
                'latitude': 33.3,
                'longitude': 33.3,
                'height': 3333
            },
            'level': {
                'winter': '',
                'summer': '2a',
                'autumn': '2b',
                'spring': ''
            },
            'images': [
                {
                    'data': 'http://www.passages.com/passage31.jpg',
                    'title': 'Перевал-3-1'
                },
                {
                    'data': 'https://www.passages.com/passage32.jpg',
                    'title': 'Перевал-3-2'
                }
            ]
        }
        json_data = json.dumps(data)
        response = self.client.post(reverse('passage-list'), data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Passage.objects.all().count(), 3)
        self.assertEqual(User.objects.all().count(), 2)

    # проверяем отсутствие создания записи о перевале при незаполненных обязательных полях
    def test_invalid_create(self):
        data = {
            'beauty_title': 'перевал',
            'title': '',
            'other_titles': 'Перевал4',
            'connect': 'Соединяет4',
            'user': {
                'email': '',
                'fam': '',
                'name': '',
                'otc': '',
                'phone': ''
            },
            'coords': {
                'latitude': 44.4,
                'longitude': 44.4,
                'height': 4444
            },
            'level': {
                'winter': '1a',
                'summer': '1a',
                'autumn': '1a',
                'spring': '1a'
            },
            'images': [
                {
                    'data': 'http://www.passages.com/passage41.jpg',
                    'title': 'Перевал-4-1'
                },
            ],
            'status': 'new'
        }
        json_data = json.dumps(data)
        response = self.client.post(reverse('passage-list'), data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Passage.objects.all().count(), 2)

    # проверяем обновление разрешенных данных
    def test_valid_update(self):
        data = {
            'beauty_title': 'перевал',
            'title': 'Перевал1',
            'other_titles': 'Перевал1',
            'connect': 'Соединяет1',
            'user': {
                'email': 'email1@gmail.com',
                'fam': 'Фамилия1',
                'name': 'Имя1',
                'otc': 'Отчество1',
                'phone': '89271001010'
            },
            'coords': {
                'latitude': 55.5,
                'longitude': 55.5,
                'height': 5555
            },
            'level': {
                'winter': '3b',
                'summer': '2b',
                'autumn': '3a',
                'spring': '3b'
            },
            'images': [
                {
                    'data': 'http://www.passages.com/passage11.jpg',
                    'title': 'Перевал-1-1'
                },
                {
                    'data': 'http://www.passages.com/passage12.jpg',
                    'title': 'Перевал-1-2'
                },
                {
                    'data': 'http://www.passages.com/passage13.jpg',
                    'title': 'Перевал-1-3'
                },
            ],
            'status': 'accepted'
        }

        json_data = json.dumps(data)
        response = self.client.patch(
            reverse('passage-detail',kwargs={'pk': self.passage1.id}),
            data=json_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.passage1.refresh_from_db()
        self.assertEqual('Перевал1', self.passage1.other_titles)
        self.assertEqual('Соединяет1', self.passage1.connect)
        self.assertEqual(55.5, self.passage1.coords.latitude)
        self.assertEqual(55.5, self.passage1.coords.longitude)
        self.assertEqual(5555, self.passage1.coords.height)
        self.assertEqual('3b', self.passage1.level.winter)
        self.assertEqual('2b', self.passage1.level.summer)
        self.assertEqual('3a', self.passage1.level.autumn)
        self.assertEqual('3b', self.passage1.level.spring)
        self.assertEqual('accepted', self.passage1.status)

    # проверяем отсутствие обновления разрешенных данных, если статус не new
    def test_invalid_update_if_status_is_not_new(self):
        data = {
            'beauty_title': 'перевал',
            'title': 'Перевал2',
            'other_titles': '',
            'connect': 'Соединяет2',
            'user': {
                'email': 'email2@gmail.com',
                'fam': 'Фамилия2',
                'name': 'Имя2',
                'otc': '',
                'phone': '89272002020'
            },
            'coords': {
                'latitude': 22.2,
                'longitude': 22.2,
                'height': 2222
            },
            'level': {
                'winter': '',
                'summer': '1b',
                'autumn': '1b',
                'spring': ''
            },
            'images': [
                {
                    'data': 'http://www.passages.com/passage21.jpg',
                    'title': 'Перевал-2-1'
                },
                {
                    'data': 'http://www.passages.com/passage22.jpg',
                    'title': 'Перевал-2-2'
                },
                {
                    'data': 'http://www.passages.com/passage23.jpg',
                    'title': 'Перевал-2-3'
                },
            ],
            'status': 'pending'
        }

        json_data = json.dumps(data)
        response = self.client.patch(
            reverse('passage-detail', kwargs={'pk': self.passage2.id}),
            data=json_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.passage2.refresh_from_db()
        self.assertEqual('', self.passage2.connect)

    # проверяем отсутствие возможности изменить данные пользователя
    def test_user_update(self):
        data = {
            'user': {
                'email': 'email3@mail.ru',
                'fam': 'Фамилия3',
                'name': 'Имя3',
                'otc': 'Отчество3',
                'phone': '89273003030'
            },
            'beauty_title': 'перевал',
            'title': 'Перевал1',
            'other_titles': '',
            'connect': '',
            'coords': {
                'latitude': 11.1,
                'longitude': 11.1,
                'height': 1111
            },
            'level': {
                'winter': '',
                'summer': '1a',
                'autumn': '1a',
                'spring': ''
            },
            'status': 'new',
            'images': [
                {
                    'data': 'http://www.passages.com/passage1-1.jpg',
                    'title': 'Перевал-1-1'
                },
                {
                    'data': 'http://www.passages.com/passage1-2.jpg',
                    'title': 'Перевал-1-2'
                },
                {
                    'data': 'http://www.passages.com/passage1-3.jpg',
                    'title': 'Перевал-1-3'
                },
            ]
        }
        json_data = json.dumps(data)
        response = self.client.patch(
            reverse('passage-detail', kwargs={'pk': self.passage1.id}),
            data=json_data,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.passage1.refresh_from_db()
        self.assertEqual('email1@gmail.com', self.passage1.user.email)
        self.assertEqual('Фамилия1', self.passage1.user.fam)
        self.assertEqual('Имя1', self.passage1.user.name)
        self.assertEqual('Отчество1', self.passage1.user.otc)
        self.assertEqual('89271001010', self.passage1.user.phone)
