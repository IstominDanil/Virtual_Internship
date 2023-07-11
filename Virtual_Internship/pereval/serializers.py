from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from .models import Passage, User, Level, Coords, Images


# сериализатор вложенной модели уровней сложности перевала
class LevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Level
        fields = [
            'winter',
            'summer',
            'autumn',
            'spring',
        ]


# сериализатор вложенной модели географичеких координат перевала
class CoordsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coords
        fields = [
            'latitude',
            'longitude',
            'height',
        ]


# сериализатор вложенной модели пользователя, создающего запись о перевале
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'email',
            'fam',
            'name',
            'otc',
            'phone',
        ]

    def save(self, **kwargs):
        self.is_valid()
        user = User.objects.filter(email=self.validated_data.get('email'))
        if user.exists():
            return user.first()
        else:
            new_user = User.objects.create(
                fam=self.validated_data.get('fam'),
                name=self.validated_data.get('name'),
                otc=self.validated_data.get('otc'),
                phone=self.validated_data.get('phone'),
                email=self.validated_data.get('email'),
            )
            return new_user


# сериализатор модели фотографий, прикрепляемых к перевалу
class ImagesSerializer(serializers.ModelSerializer):
    data = serializers.URLField(label='URL')

    class Meta:
        model = Images
        fields = [
            'data',
            'title',
        ]


# сериализатор модели самого перевала
class PassageSerializer(WritableNestedModelSerializer):
    coords = CoordsSerializer()
    level = LevelSerializer()
    user = UserSerializer()
    images = ImagesSerializer(many=True)

    class Meta:
        model = Passage
        depth = 1
        fields = [
            'id',
            'beauty_title',
            'title',
            'other_titles',
            'connect',
            'user',
            'coords',
            'level',
            'images',
            'status',
        ]

    # переопределяем метод post
    def create(self, validated_data, **kwargs):
        user = validated_data.pop('user')
        coords = validated_data.pop('coords')
        level = validated_data.pop('level')
        images = validated_data.pop('images')

        user_ = User.objects.filter(email=user['email'])
        if user_.exists():
            user_serializer = UserSerializer(data=user)
            user_serializer.is_valid(raise_exception=True)
            user = user_serializer.save()
        else:
            user = User.objects.create(**user)

        coords = Coords.objects.create(**coords)
        level = Level.objects.create(**level)
        passage = Passage.objects.create(**validated_data, user=user, coords=coords, level=level)
        if images:
            for image in images:
                data = image.pop('data')
                title = image.pop('title')
                Images.objects.create(data=data, passage=passage, title=title)

        return passage

    def validate(self, data):
        if self.instance is not None:
            instance_user = self.instance.user
            data_user = data.get('user')
            user_fields_for_validation = [
                instance_user.fam != data_user['fam'],
                instance_user.name != data_user['name'],
                instance_user.otc != data_user['otc'],
                instance_user.phone != data_user['phone'],
                instance_user.email != data_user['email'],
            ]
            if data_user is not None and any(user_fields_for_validation):
                raise serializers.ValidationError(
                    {
                        'Отказано': 'Данные пользователя не могут быть изменены',
                    }
                )
        return data