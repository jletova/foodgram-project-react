from django.core.mail import send_mail
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model

from rest_framework import viewsets, status, filters
from rest_framework import generics, mixins, views
from rest_framework.mixins import CreateModelMixin, ListModelMixin

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action

# from api_yamdb.settings import PROJECT_MAIL

from .serializers import (UserSerializer, 
    TagSerializer, IngredientSerializer, RecipeSerializer,
    IngredientsAmountSerializer)
#     UserSerializer, UserAuthSerializer, UserTokenSerializer,
#     FollowSerializer, TagSerializer,
#     RecipeSerializer, IngredientSerializer
# )
# from .permissions import (AdminRoleOnly, ReadOnly,
                        #   IsAuthorModeratorAdminOrReadOnly)
from api.models import User, Tag, Ingredient, Recipe
# from api.filters import TitleFilter


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Класс-вьюсет для модели User."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (AdminRoleOnly,)
    # permission_classes = (AllowAny,)
    # lookup_field = 'id'
    # filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('email', 'username')


class RecipeViewSet(viewsets.ModelViewSet):
    """View-функция для произведений."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [AllowAny]
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = RecipeFilter

    # def get_queryset(self):
    #     print('asdfasdf', self.request)
    #     if self.request.method == "GET":
    #         return Ingredient.objects.order_by('-id').annotate(amount=F('ingredient__amount'))
    #     return Recipe.objects.all()

    # def get_serializer_class(self):
    #     if self.request.method == "GET":
    #         return ReadRecipeSerializer
    #     return WrireRecipeSerializer


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """View-функция для категорий."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['=name']
    # lookup_field = 'id'


# class CreateDeleteViewSet (mixins.CreateModelMixin,
#                            mixins.DeleteModelMixin,
#                            viewsets.GenericViewSet):
#     pass


# class AddDeleteFollowViewSet(CreateDeleteViewSet):
#     serializer_class = FollowSerializer
#     permission_classes = [IsAuthorModeratorAdminOrReadOnly, ]
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('following__username',)

#     def get_following(self):
#         return get_object_or_404(User, pk=self.kwargs.get('user_id'))

#     def perform_create(self, serializer):
#         serializer.save(
#             user=self.request.user,
#             is_subscribed=True,
#             # following=self.get_following()
#         )
#         return self.get_following()

#     def perform_destroy(self, instance):
#         # Follow.objects.delete(user=self.request.user, following=self.get_following())
#         instance.delete()
#         # return self.get_object(is_subscribed=False)
#         instance.delete(is_subscribed=False)
#         # return self.get_following(is_subscribed=False)


# class FollowViewSet(ListAPIView):
#     serializer_class = FollowSerializer
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('following__username',)

#     def get_queryset(self):
#         return self.request.user.is_subscribed.all()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """View-функция для ингридиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = 'pk'


# class IngredientsAmountViewSet(viewsets.ModelViewSet):
#     """View-функция для ингридиентов в рецепте."""
#     queryset = Ingredient.objects.order_by('-id').annotate(amount=F('ingredient__amount'))
#     # queryset = IngredientsAmount.objects.all()
#     serializer_class = IngredientSerializer
#     permission_classes = [AllowAny]
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['=name']
#     lookup_field = 'pk'

# if self.context['request'].user.is_authenticated: