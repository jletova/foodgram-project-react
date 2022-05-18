from multiprocessing import context
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator

from rest_framework import serializers
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from rest_framework.exceptions import ValidationError

from drf_extra_fields.fields import Base64ImageField


from api.models import User, Tag, Ingredient, Recipe, IngredientsAmount


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

    class Meta:
        fields = ('email', 'id', 'username', 'first_name', 'last_name')
        model = User


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для  тагов."""

    class Meta:
        fields = '__all__'
        model = Tag


class TagField(serializers.PrimaryKeyRelatedField):
    """Кастомное поле для тэгов."""

    def to_representation(self, value):
        return TagSerializer(value).data


class ImageField(Base64ImageField):
    """Кастомное поле для картинок."""

    def to_internal_value(self, base64_data):
        return Base64ImageField(base64_data)



class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для сериализации ингредиентов."""

    class Meta:
        fields = '__all__'
        model = Ingredient


class IngredientsAmountSerializer(serializers.ModelSerializer):
    '''Сериализатор для ингредиентов в рецепте.'''

    id =  serializers.IntegerField()

    class Meta:
        model = IngredientsAmount
        fields = ('id', 'amount')

    def to_representation(self, instance):
        # instance = объект модели IngredientsAmount (ngredient, recipe, amount)
        representation = IngredientSerializer(instance.ingredient).data
        representation['amount'] = instance.amount
        return representation 


class RecipeSerializer(serializers.ModelSerializer):
    """Класс для сериализации рецептов."""
    author = UserSerializer(many=False, read_only=True)
    ingredients = IngredientsAmountSerializer(source='ingredient', many=True)
    tags = TagField(queryset=Tag.objects.all(), many=True)
    image = Base64ImageField()

    class Meta:
        fields = '__all__'
        model = Recipe

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredient')
        tags_data = validated_data.pop('tags')
        reicpe = Recipe.objects.create(**validated_data)
        reicpe.tags.set(tags_data)
        for ingredient in ingredients_data:
            IngredientsAmount.objects.create(
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                recipe=reicpe, amount=ingredient['amount']
            )
        return reicpe


# class AddDeleteFollowSerializer(serializers.ModelSerializer):
#     """Класс для сериализации подписок."""
#     slug = serializers.SlugField(validators=[UniqueValidator(
#         queryset=Follow.objects.all())])

#     class Meta:
#         fields = ['name', 'slug']
#         model = Follow


# class FollowField(serializers.SlugRelatedField):
#     """Поле для вывода подписки."""

#     def 
# (self, value):
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




        # recipe = super().create(validated_data)
