from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .filters import CustomFilter, IngredientSearchFilter
from .models import (FavouriteRecipe, Follow, Ingredient, IngredientsAmount,
                     IsInShoppingCart, Recipe, Tag)
from .pagination import CustomPagination
from .permissions import AdminOrReadOnly, IsAuthorAdminOrReadOnly
from .serializers import (IngredientSerializer, RecipeSerializer,
                          ShortRecipeSerializer, TagSerializer,
                          UserAndRecipeSerializer, UserSerializer)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Класс-вьюсет для модели User."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('email', 'username')


class IngredientViewSet(viewsets.ModelViewSet):
    """View-функция для ингридиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = [AdminOrReadOnly]
    filter_backends = [IngredientSearchFilter]
    search_fields = ['^name', ]


class RecipeViewSet(viewsets.ModelViewSet):
    """View-функция для произведений."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthorAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPagination
    filterset_class = CustomFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            FavouriteRecipe.objects.create(
                user=self.request.user,
                recipe=recipe
            )
            serializer = ShortRecipeSerializer(recipe)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        unsubscribe = get_object_or_404(
            FavouriteRecipe,
            user=request.user,
            recipe=recipe
        )
        unsubscribe.delete()
        return Response(
            data={"Success": "Рецепт удален из избранных"},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            IsInShoppingCart.objects.create(
                user=self.request.user,
                recipe=recipe
            )
            serializer = ShortRecipeSerializer(recipe)
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        unsubscribe = get_object_or_404(
            IsInShoppingCart,
            user=request.user,
            recipe=recipe
        )
        unsubscribe.delete()
        return Response(
            data={"Success": "Рецепт удален из списка покупок"},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def download_shopping_cart(self, request):
        recipes = list(
            request.user.shopping_cart.all()
            .values_list('recipe__id', flat=True)
        )
        ingredients = (
            IngredientsAmount.objects.filter(recipe__in=recipes)
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(amount=Sum('amount'))
        )
        data = ingredients.values_list(
            'ingredient__name',
            'ingredient__measurement_unit',
            'amount'
        )
        cart = 'СПИСОК ПОКУПОК:\n'
        for name, measure, amount in data:
            cart += (
                f'• {name.capitalize()} ({measure}) — {amount}\n'
            )
        response = HttpResponse(
            cart,
            content_type='text/plain;charset=UTF-8',
        )
        response['Content-Disposition'] = (
            'attachment;'
            'filename="shopping_cart.txt"'
        )
        return response


class TagViewSet(viewsets.ModelViewSet):
    """View-функция для категорий."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AdminOrReadOnly, ]
    pagination_class = None
    filter_backends = [filters.SearchFilter]
    search_fields = ['^name', 'slug']


class FollowViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserAndRecipeSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return User.objects.filter(follow__user=self.request.user)


@permission_classes([IsAuthenticated])
@api_view(['DELETE', 'POST'])
def subscribe(request, user_id):
    """View-функция для создания и удаления подписок."""
    following = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        Follow.objects.create(
            user=request.user,
            following=following
        )
        serializer = UserAndRecipeSerializer(following)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )
    unsubscribe = get_object_or_404(
        Follow,
        user=request.user,
        following=following
    )
    unsubscribe.delete()
    return Response(
        data={"Success": "Подписка удалена"},
        status=status.HTTP_200_OK
    )
