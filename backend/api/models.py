from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомный класс для пользователей."""
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта'
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Никнейм'
    )
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    password = models.CharField(max_length=150, verbose_name='Пароль')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Ingredient(models.Model):
    """Ингридиенты для рецептов."""
    name = models.CharField(
        max_length=200,
        blank=False,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=200,
        blank=False,
        verbose_name='Единицы изменения'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
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
    name = models.CharField(
        max_length=200,
        blank=False,
        unique=True,
        verbose_name='Название'
    )
    color = models.CharField(max_length=7, verbose_name='Цвет',
                             help_text='HEX color, as #RRGGBB')
    slug = models.SlugField(max_length=200, blank=False,
                            unique=True, verbose_name='Слаг')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Рецепты."""
    author = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        default='Пользователь больше не существует',
        related_name='recipe',
        blank=False,
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=200,
        blank=False,
        verbose_name='Название'
    )
    text = models.TextField(
        blank=False,
        verbose_name='Текст'
    )
    image = models.ImageField(upload_to='recipes/', blank=False, null=False,
                              verbose_name='Изображение')
    cooking_time = models.PositiveIntegerField(
        blank=False,
        verbose_name='Время приготовления'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='recipe',
        verbose_name='Теги'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientsAmount',
        related_name='recipe',
        verbose_name='Ингридиенты'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
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
        blank=False,
        verbose_name='Рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Количество'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient',
        blank=False,
        verbose_name='Ингридиент'
    )

    class Meta:
        ordering = ['-ingredient']
        verbose_name = 'Количество'
        verbose_name_plural = ''
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
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Рецепт'
    )

    class Meta:
        ordering = ['-user']
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзина покупок'
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
        verbose_name='Пользователь'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follow',
        blank=False, null=False,
        verbose_name='Подписан на'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
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
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favouriterecipe',
        blank=False, null=False,
        verbose_name='Рецепт'
    )

    class Meta:
        ordering = ['-user']
        verbose_name = 'Любимый рецепт'
        verbose_name_plural = 'Любимые рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_follow_recipe'
            )
        ]
