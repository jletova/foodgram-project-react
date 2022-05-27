from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомный класс для пользователей."""
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=150, unique=True)  # ^[\w.@+-]+\z
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.username


class Ingredient(models.Model):
    """Ингридиенты для рецептов."""
    name = models.CharField(max_length=200, blank=False)
    measurement_unit = models.CharField(max_length=200, blank=False)

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient_and_measurement'
            ),
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Тэги для рецептов."""
    name = models.CharField(max_length=200, blank=False, unique=True)
    color = models.CharField(max_length=7,
                             help_text='HEX color, as #RRGGBB')
    slug = models.SlugField(max_length=200, blank=False, unique=True)

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
        related_name='recipe',
        blank=False
    )
    name = models.CharField(
        max_length=200,
        blank=False,
    )
    text = models.TextField(
        blank=False,
    )
    image = models.ImageField(upload_to='recipes/')
    cooking_time = models.PositiveIntegerField(blank=False)
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='recipe',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientsAmount',
        related_name='recipe',
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


class IngredientsAmount(models.Model):
    """Количество ингридиента в рецепте."""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient',
        blank=False
    )
    amount = models.PositiveSmallIntegerField(default=1)
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient',
        blank=False
    )

    class Meta:
        ordering = ['-ingredient']
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient_in_recipe'
            ),
        ]

    def __str__(self):
        return f'{self.ingredient} = {self.amount}'


class IsInShoppingCart(models.Model):
    """Модель для списка покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
    )

    class Meta:
        ordering = ['-user']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_shopping_cart',
            )
        ]

    def __str__(self):
        return f'{self.user} - {self.recipe}'


class Follow(models.Model):
    """Подписки."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followuser',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follow',
        blank=False, null=False
    )

    class Meta:
        ordering = ['-id']
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
    """Список избранного."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favouriterecipe',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favouriterecipe',
        blank=False, null=False
    )

    class Meta:
        ordering = ['-user']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_follow_recipe'
            )
        ]
