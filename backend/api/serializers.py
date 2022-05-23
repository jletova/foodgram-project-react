from asyncore import read
from multiprocessing import context
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from pkg_resources import require

from rest_framework import serializers, viewsets, mixins, generics
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from rest_framework.exceptions import ValidationError

from djoser.serializers import UserSerializer as DjoserUserSerializer
from drf_extra_fields.fields import Base64ImageField


from api.models import User, Tag, Ingredient, Recipe, IngredientsAmount, Follow


User = get_user_model()


class UserSerializer(DjoserUserSerializer):
    """Сериализатор для модели User."""

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')
        model = User

    def get_is_subscribed(self, obj):
        if not self.context['request'].user.is_authenticated:
            return False
        user = self.context['request'].user
        return Follow.objects.filter(user=user, following=obj).exists()


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
        # instance = объект модели IngredientsAmount (igredient, recipe, amount)
        representation = IngredientSerializer(instance.ingredient).data
        representation['amount'] = instance.amount
        return representation 


class RecipeSerializer(serializers.ModelSerializer):
    """Класс для сериализации рецептов."""
    author = UserSerializer(many=False, read_only=True)
    # ingredients = IngredientsAmountSerializer(source='ingredient', many=True)
    tags = TagSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        # fields = '__all__'
        exclude=('ingredients',  )
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


class RecipesInFollowSerializer(serializers.ModelSerializer):
    """Сериализатор User для подписок."""

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe


class UserAndRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор User для подписок."""
    recipes = serializers.SerializerMethodField(read_only=True)
    # recipes = RecipesInFollowSerializer(
    #     many=True,
    #     read_only=True,
    #     queryset=Recipe.objects.filter(author=User)
    # )
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        fields = ('email', 'id', 'username', 'first_name', 
            'last_name', 'recipes', 'recipes_count')
        model = User
    
    # def get_limit_object(self, obj):
    #     recipes_limit = self.context['recipes_limit']
    #     limit = (int(recipes_limit)
    #              if recipes_limit and recipes_limit.isdigit()
    #              else None)
    #     return self.get_object(obj)[:limit]

    def get_recipes_count(self, obj):
        return obj.recipe.count()
    
    def get_recipes(self, obj):
        recipes = obj.recipe.all()
        # recipes = self.get_limit_object(obj)
        serializer = RecipesInFollowSerializer(
            instance=recipes,
            many=True
        )
        return serializer.data


class FollowSerializer(serializers.ModelSerializer):
    # following = UserAndRecipeSerializer(read_only=True)
    following = UserAndRecipeSerializer()

    class Meta:
        fields = ('following', )
        model = Follow
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation.get('following')


# recipes_limit передаю при создании экземпляра в context

# def get_object(self, obj):
#         return Recipes.objects.filter(
#             author=obj
#         )