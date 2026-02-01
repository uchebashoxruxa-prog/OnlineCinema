from rest_framework import serializers
from online_cinema.models import Category, Comment, Cinema, Actor


# class CategoryListSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField()
#
#
# class CinemaListSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField()
#     description = serializers.CharField(max_length=150)
#     photo = serializers.ImageField()
#     category = CategoryListSerializer(many=True, read_only=True)
#     count_views = serializers.IntegerField()
#     count_comment = serializers.IntegerField()
#
#
# class ActorSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     full_name = serializers.CharField()
#     avatar = serializers.ImageField()
#
# class CommentListSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     text = serializers.CharField()
#     updated_at = serializers.DateTimeField()
#     author = serializers.CharField()
#     author_id = serializers.IntegerField()
#     author_photo = serializers.CharField()
#
#
# class CinemaDetailSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField()
#     description = serializers.CharField(max_length=150)
#     photo = serializers.ImageField()
#     category = CategoryListSerializer(many=True, read_only=True)
#     count_views = serializers.IntegerField()
#     count_comment = serializers.IntegerField()
#     video = serializers.FileField()
#     trailer = serializers.CharField()
#     year = serializers.CharField()
#     country = serializers.CharField()
#     released = serializers.CharField()
#     actors = ActorSerializer(many=True, read_only=True)
#     comments = CommentListSerializer(many=True, read_only=True)
#
#
#
# class CommentCreateSerializer(serializers.Serializer):
#     text = serializers.CharField()
#     author_id = serializers.IntegerField(required=False)
#     cinema_id = serializers.IntegerField(required=False)
#
#     def create(self, validated_data):  # {"text": "comment", "author_id": 1, "cinema_id": 5}
#         return Comment.objects.create(**validated_data)
#
#
#     def update(self, instance, validated_data): # comment_ob, {"text": "comment"}
#         instance.text = validated_data.get('text', instance.text)
#         instance.author_id = instance.author_id
#         instance.cinema_id = instance.cinema_id
#         instance.save()
#         return instance
#
#
#
# class ProfileSerializer(serializers.Serializer):
#     is_online = serializers.BooleanField()
#     photo = serializers.ImageField()
#     about = serializers.CharField()
#     location = serializers.CharField()
#
#
# class AuthUserSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     username = serializers.CharField()
#     first_name = serializers.CharField()
#     last_name = serializers.CharField()
#     email = serializers.EmailField()
#     date_joined = serializers.DateTimeField(format='%H:%M %d.%m.%Y')
#     last_login = serializers.DateTimeField(format='%H:%M %d.%m.%Y')
#     profileuser = ProfileSerializer(read_only=True)

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CinemaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cinema
        fields = ('title', 'description', 'photo', 'count_comment', 'count_views')


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = "__all__"


# Класс сериализация и получения подкомментариев
class RecursiveSerializer(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


# Класс Сериалайзер для фильтрации
class FilterCommentSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)

class CommentCinemaSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField('username', read_only=True)
    created_at = serializers.DateTimeField(format="%H:%M  %d.%m.%Y")
    author_photo = serializers.CharField()
    author_id = serializers.IntegerField()
    sub_comments = RecursiveSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        list_serializer_class = FilterCommentSerializer
        exclude = ('updated_at',)


class CinemaDetailSerializer(serializers.ModelSerializer):
    count_comment = serializers.IntegerField()
    count_views = serializers.IntegerField()
    category = CategoryListSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)
    comments = CommentCinemaSerializer(many=True, read_only=True)

    class Meta:
        model = Cinema
        exclude = ('views', 'created_at', 'updated_at')


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('text', 'cinema', 'author', 'parent')
