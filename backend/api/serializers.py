from ast import Raise
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer as DjoserUserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.models import (FavouriteRecipe, Follow, Ingredient, IngredientsAmount,
                        IsInShoppingCart, Recipe, Tag)

User = get_user_model()


class UserSerializer(DjoserUserSerializer):
    """Сериализатор для модели User."""

    is_subscribed = serializers.SerializerMethodField(read_only=True)
    # username = serializers.CharField(
    #     max_length=150, required=True,
    #     validators=[
    #         RegexValidator(
    #             regex='^[\w.@+-]+\z',
    #             message='Invalid username',
    #             code='invalid_username'
    #         ),
    #     ]
    # )

    class Meta:
        fields = ('email', 'id', 'username',
            'first_name', 'last_name', 'is_subscribed')
        model = User

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return Follow.objects.filter(user=user, following=obj).exists()


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов."""

    class Meta:
        fields = '__all__'
        model = Tag

    def to_internal_value(self, data):
        return Tag.objects.get(id=data)


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для сериализации ингредиентов."""

    class Meta:
        fields = '__all__'
        model = Ingredient


class IngredientsAmountSerializer(serializers.ModelSerializer):
    '''Сериализатор для ингредиентов в рецепте.'''

    id = serializers.IntegerField()

    class Meta:
        model = IngredientsAmount
        fields = ('id', 'amount')

    def to_representation(self, instance):
        representation = IngredientSerializer(instance.ingredient).data
        representation['amount'] = instance.amount
        return representation


class RecipeSerializer(serializers.ModelSerializer):
    """Класс для сериализации рецептов."""
    author = UserSerializer(many=False, read_only=True)
    ingredients = IngredientsAmountSerializer(source='ingredient', many=True)
    tags = TagSerializer(many=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Recipe

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if not user.is_authenticated or self.context.get('request') is None:
            return False
        return FavouriteRecipe.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if not user.is_authenticated or self.context.get('request') is None:
            return False
        return IsInShoppingCart.objects.filter(user=user, recipe=obj).exists()

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredient')
        tags_data = validated_data.pop('tags')
        reicpe = Recipe.objects.create(**validated_data)
        reicpe.tags.set(tags_data)
        for item in ingredients_data:
            IngredientsAmount.objects.create(
                ingredient=get_object_or_404(Ingredient, id=item['id']),
                recipe=reicpe, amount=item['amount']
            )
        return reicpe

    def update(self, recipe, validated_data):
        IngredientsAmount.objects.filter(recipe=recipe).delete()
        ingredients_data = validated_data.pop('ingredient')
        tags_data = validated_data.pop('tags')
        recipe.tags.set(tags_data)
        for item in ingredients_data:
            IngredientsAmount.objects.create(
                ingredient=get_object_or_404(Ingredient, id=item['id']),
                recipe=recipe, amount=item['amount']
            )
        try:
            recipe.text = validated_data.get('text')
            recipe.name = validated_data.get('name')
            recipe.cooking_time = validated_data.get('cooking_time')
            recipe.image = validated_data.get('image')
            recipe.save()
        except ValidationError:
            Raise ('Все поля обязательны для заполнения')
        return recipe


class ShortRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор User для подписок."""

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe


class UserAndRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор User для подписок."""
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'recipes', 'recipes_count')
        model = User

    def get_recipes_count(self, obj):
        return obj.recipe.count()

    def get_recipes_limit(self):
        recipes_limit = self.context['request'].query_params['recipes_limit']
        return int(recipes_limit)

    def get_recipes(self, obj):
        if 'recipes_limit' in str(self.context['request']):
            limit = self.get_recipes_limit()
        recipes = obj.recipe.all()[:limit]
        serializer = ShortRecipeSerializer(
            instance=recipes,
            many=True
        )
        return serializer.data
