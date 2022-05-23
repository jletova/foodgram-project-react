from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response

from rest_framework import viewsets, status, filters
from rest_framework import generics, mixins, views
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.pagination import PageNumberPagination

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action

# from api_yamdb.settings import PROJECT_MAIL

from .serializers import (UserSerializer, RecipesInFollowSerializer,
    TagSerializer, IngredientSerializer, RecipeSerializer,
    FollowSerializer, UserAndRecipeSerializer)

from .permissions import IsAuthorAdminOrReadOnly
# (AdminRoleOnly, ReadOnly,
                        #   IsAuthorAdminOrReadOnly)
from api.models import User, Tag, Ingredient, Recipe, Follow, FavouriteRecipe, IsInShoppingCart
# from api.filters import TitleFilter


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Класс-вьюсет для модели User."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (AdminRoleOnly,)
    permission_classes = (AllowAny,)
    # lookup_field = 'id'
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    # search_fields = ('email', 'username')

    # @action(detail=True, methods=['post', 'delete'], url_path='subscribe')
    # def subscribe(self, request, pk):
    #     """View-функция для создания и удаления подписок."""
    #     following = get_object_or_404(User, pk=pk)
    #     if request.method == 'POST':
    #         Follow.objects.create(
    #                 user=request.user,
    #                 following=following
    #             )
    #         serializer = UserAndRecipeSerializer(following)
    #         return Response(
    #             data=serializer.data,
    #             status=status.HTTP_201_CREATED
    #             )
    #     unsubscribe = get_object_or_404(
    #         Follow,
    #         user=request.user,
    #         following=following
    #     )
    #     unsubscribe.delete()
    #     return Response(
    #         data={"Success": "Подписка удалена"},
    #         status=status.HTTP_400_BAD_REQUEST
    #     )


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """View-функция для ингридиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = 'pk'


class RecipeViewSet(viewsets.ModelViewSet):
    """View-функция для произведений."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [AllowAny]
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            FavouriteRecipe.objects.create(
                    user=self.request.user,
                    recipe=recipe
                )
            serializer = RecipesInFollowSerializer(recipe)
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
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            IsInShoppingCart.objects.create(
                    user=self.request.user,
                    recipe=recipe
                )
            serializer = RecipesInFollowSerializer(recipe)
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
            status=status.HTTP_400_BAD_REQUEST
        )


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """View-функция для категорий."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['=name']
    # lookup_field = 'id'


class FollowViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthorAdminOrReadOnly]
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.followuser.all()

    def get_following(self):
        return get_object_or_404(User,
            pk=self.kwargs.get('user_id')
        )


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
        status=status.HTTP_201_CREATED
    )


#     queryset = Ingredient.objects.order_by('-id').annotate(amount=F('ingredient__amount'))

# if self.context['request'].user.is_authenticated:

    # rest_framework.permissions.CurrentUserOrAdmin
    # lookup_field = 'email'
    # lookup_value_regex = '[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}'

    # def update(self, request, *args, **kwargs):
    #     if request.method =='PUT':
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #     return super().update(request, *args, **kwargs)

    # def subscriptions(self, request):
    #     queryset = Subscription.objects.filter(user=request.user)


 
    # def get_following(self):
    #     return get_object_or_404(User,
    #         pk=self.kwargs.get('user_id')
    #     )

    # def get_object(self):
    #     return Follow.objects.filter(
    #         user=self.request.user,
    #         following=self.get_following()
    #     )

    # def perform_create(self, serializer):
    #     return serializer.save(
    #         user=self.request.user,
    #         following=self.get_following()
        # )

    # @action(methods=['DELETE'], detail=True)
    # def perform_destroy(self, instance):
    #     follow = Follow.objects.filter(
    #         user=self.request.user,
    #         following=self.get_following())
    #     return follow.delete()
