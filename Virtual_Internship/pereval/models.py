from django.db import models
from django.utils import timezone

# список возможных значений статуса для добавления перевала
STATUSES = [
    ('new', 'Новый'),
    ('pending', 'Модерируется'),
    ('accepted', 'Принят'),
    ('rejected', 'Не принят')
]

# список уровней сложности
LEVELS = [
    ('', 'Не задано'),
    ('1a', '1А'),
    ('1b', '1Б'),
    ('2a', '2А'),
    ('2b', '2Б'),
    ('3a', '3А'),
    ('3b', '3Б'),
    ('3b*', '3Б*')
]


# функция получения пути для сохранения фотографий, чтобы было понятно, к какому перевалу они относятся
def get_image_path(instance, file):
    return f'photos/pereval-{instance.passage.id}/{file}'


# Create your models here.
# модель географических координат
class Coords(models.Model):
    latitude = models.FloatField('Широта', max_length=32, blank=True, null=True)
    longitude = models.FloatField('Долгота', max_length=32, blank=True, null=True)
    height = models.IntegerField('Высота', blank=True, null=True)

    def __str__(self):
        return f'широта: {self.latitude}, долгота: {self.longitude}, высота: {self.height}'


# модель уровней сложности для разных сезонов
class Level(models.Model):
    winter = models.CharField('Зима', choices=LEVELS, max_length=5, default='')
    summer = models.CharField('Лето', choices=LEVELS, max_length=5, default='')
    autumn = models.CharField('Осень', choices=LEVELS, max_length=5, default='')
    spring = models.CharField('Весна', choices=LEVELS, max_length=5, default='')

    def __str__(self):
        return f'зима: {self.winter}, лето: {self.summer}, осень: {self.autumn}, весна: {self.spring}'


# модель пользователя
class User(models.Model):
    email = models.EmailField('Email', max_length=128)
    phone = models.CharField('Телефон', max_length=12)
    fam = models.CharField('Фамилия', max_length=64)
    name = models.CharField('Имя', max_length=64)
    otc = models.CharField('Отчество', max_length=64, blank=True, null=True)

    def __str__(self):
        return f'{self.fam} {self.name} {self.otc}'


# модель добавления перевала
class Passage(models.Model):
    add_time = models.DateTimeField(default=timezone.now, editable=False)
    beauty_title = models.CharField('Префикс', default='пер.', max_length=255)
    title = models.CharField('Название', max_length=255)
    other_titles = models.CharField('Другое название', max_length=255, blank=True, null=True)
    connect = models.TextField('Что соединяет', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    coords = models.OneToOneField(Coords, on_delete=models.CASCADE, blank=True, null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField('Статус', max_length=8, choices=STATUSES, default='new')

    def __str__(self):
        return f'{self.pk}: {self.beauty_title} {self.title}'


# модель изображений перевала
class Images(models.Model):
    title = models.CharField('Название', max_length=255, blank=True, null=True)
    add_time = models.DateTimeField(default=timezone.now, editable=False)
    passage = models.ForeignKey(Passage, on_delete=models.CASCADE, related_name='images', blank=True, null=True)
    data = models.ImageField('Изображение', upload_to=get_image_path, blank=True, null=True)

    def __str__(self):
        return f'{self.pk}: {self.title} {self.data}'