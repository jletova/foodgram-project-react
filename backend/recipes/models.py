from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime as dt


CURRENT_YEAR = dt.datetime.now().year


class User(AbstractUser):
    """Кастомный класс для пользователей."""
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=150, unique=True)  # ^[\w.@+-]+\z
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'username', 'last_name', 'email', 'password']

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.username


class Ingredient(models.Model):
    """Ингридиенты для рецептов."""
    name = models.CharField(max_length=200, verbose_name='Название', blank=False, unique=True)
    measurement_unit = models.SlugField(max_length=200, blank=False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Ингридиенты для рецептов."""
    name = models.CharField(max_length=200, verbose_name='Название', blank=False, unique=True)
    color = models.CharField(verbose_name='Цвет', max_length=7,
                             help_text='HEX color, as #RRGGBB')
    slug = models.SlugField(max_length=200, blank=False, unique=True)  #^[-a-zA-Z0-9_]+$

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Рецепты."""
    author = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default='Пользователь больше не существует',
        related_name='Автор рецепта',
        blank=False
    )
    name = models.CharField(
        max_length=200,
        blank=False,
        verbose_name='Название'
    )
    text = models.TextField(
        blank=False,
        verbose_name='Описание'
    )
    image = models.ImageField(upload_to='foodgraam/media/recipes/', null=True, blank=True)  # поле для картинки
    cooking_time = models.PositiveIntegerField(blank=False)
    tags = models.ForeignKey(
        Tag,
        null=True,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Тэги'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        # null=True,
        # on_delete=models.DO_NOTHING,
        related_name='recipes',
        verbose_name='Ингредиенты'
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'author', 'text'],
                name='unique_recipe'
            ),
        ]

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    """Ингридиенты для рецептов."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='Автор рецепта',
        blank=False
    )
    amount = models.PositiveSmallIntegerField()
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='Автор рецепта',
        blank=False
    )

    class Meta:
        ordering = ['-ingredient']
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'amount', 'ingredient'],
                name='unique_ingredient_in_recipe'
            ),
        ]


class IsInShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='is_in_shopping_cart',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='is_in_shopping_cart',
    )
    # is_in_shopping_cart = models.BooleanField(default=False, blank=False)
    # is_favourite = models.BooleanField(default=False, blank=False)


    class Meta:
        ordering = ['-user']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_shopping_cart',
            ),
            # models.UniqueConstraint(
            #     fields=['user', 'recipe'], name='unique_favourite',
            # ),
        ]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='is_subscribed',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='is_subscribed',
        blank=False, null=False
    )

    class Meta:
        ordering = ['-user']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'], name='unique_follow'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='self_following'
            )
        ]

    def __str__(self):
        return f'{self.user} подписан на {self.following}'


class FavouriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='is_favourite',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='is_favourite',
        blank=False, null=False
    )

    class Meta:
        ordering = ['-user']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_follow_recipe'
            )
        ]