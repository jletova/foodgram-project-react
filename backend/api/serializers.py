# from django.contrib.auth import get_user_model
# from django.shortcuts import get_object_or_404
# from django.contrib.auth.tokens import default_token_generator

# from rest_framework import serializers
# from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
# from rest_framework.exceptions import ValidationError

# from foodgram.models import Recipe, Ingredient, Follow, Tag


# User = get_user_model()


# class UserSerializer(serializers.ModelSerializer):
#     """Класс для сериализации модели User."""

#     class Meta:
#         fields = '__all__'
#         model = User


# class UserTokenSerializer(serializers.Serializer):
#     """Класс для сериализации модели User при выдаче JWT токена."""
#     confirmation_code = serializers.CharField()
#     username = serializers.CharField(max_length=150)

#     def validate(self, attrs):
#         """Валидация входных данных при выдаче токена."""
#         user = get_object_or_404(User, username=attrs['username'])
#         if not default_token_generator.check_token(
#             user, attrs['confirmation_code']
#         ):

#             raise serializers.ValidationError(
#                 'Ваш токен невалидный или устарел!'
#             )
#         return attrs


# class RecipeSerializer(serializers.ModelSerializer):
#     """Класс для сериализации тайтлов."""
#     category = CategoryField(
#         queryset=Category.objects.all(),
#         slug_field='slug'
#     )
#     genre = GenreField(
#         queryset=Genre.objects.all(),
#         many=True,
#         slug_field='slug'
#     )
#     rating = serializers.IntegerField(default=None, read_only=True)

#     class Meta:
#         fields = '__all__'
#         model = Recipe


# class CommentSerializer(serializers.ModelSerializer):
#     """Класс для сериализации комментариев."""
#     author = serializers.SlugRelatedField(
#         read_only=True, slug_field='username')

#     class Meta:
#         exclude = ['review']
#         read_only_fields = ('author', 'pub_date')
#         model = Comment
#         ordering = ['-id']


# class ReviewSerializer(serializers.ModelSerializer):
#     """Класс для сериализации отзывов на произведения."""
#     author = serializers.SlugRelatedField(
#         read_only=True, slug_field='username')
#     score = serializers.IntegerField(max_value=10, min_value=1)

#     class Meta:
#         exclude = ['title']
#         read_only_fields = ('author', 'pub_date', 'title')
#         model = Review
#         ordering = ['-id']

#     def validate(self, data):
#         if self.context['request'].method != "POST":
#             return data
#         title = self.context['request'].parser_context['kwargs']['title_id']
#         author = self.context['request'].user
#         if Review.objects.filter(author=author, title__id=title):
#             raise ValidationError('Ваш отзыв на это произведение уже есть')
#         return data

# # ------------

# class IngredientSerializer(serializers.ModelSerializer):
#     """Класс для сериализации ингредиентов."""
#     # slug = serializers.SlugField(validators=[UniqueValidator(
#     #     queryset=Ingredient.objects.all())])

#     class Meta:
#         fields = '__all__'
#         model = Ingredient


# class TagSerializer(serializers.ModelSerializer):
#     """Класс для сериализации тагов."""

#     class Meta:
#         fields = '__all__'
#         model = Tag


# class AddDeleteFollowSerializer(serializers.ModelSerializer):
#     """Класс для сериализации подписок."""
#     slug = serializers.SlugField(validators=[UniqueValidator(
#         queryset=Follow.objects.all())])

#     class Meta:
#         fields = ['name', 'slug']
#         model = Follow


# class FollowField(serializers.SlugRelatedField):
#     """Поле для вывода подписки."""

#     def to_representation(self, value):
#         return UserSerializer(value).data


# class FollowSerializer(serializers.ModelSerializer):
#     user = serializers.SlugRelatedField(
#         slug_field='id',
#         read_only=True,
#         default=serializers.CurrentUserDefault(),
#     )
#     # following = serializers.SlugRelatedField(
#     #     queryset=User.objects.all(),
#     #     slug_field='id',
#     # )
#     following = FollowField(
#         queryset=User.objects.all(),
#         many=True,
#         slug_field='id'
#     )

#     class Meta:
#         fields = '__all__'
#         model = Follow
#         validators = [
#             UniqueTogetherValidator(
#                 queryset=Follow.objects.all(),
#                 fields=['user', 'following'],
#             ),
#         ]

#     def validate_following(self, value):
#         if value == self.context['request'].user:
#             raise serializers.ValidationError(
#                 "Нельзя подписаться на себя"
#             )
#         return value