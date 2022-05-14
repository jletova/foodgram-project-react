# from django.core.mail import send_mail
# from django.db.models import Avg
# from django_filters.rest_framework import DjangoFilterBackend
# from django.shortcuts import get_object_or_404
# from django.contrib.auth.tokens import default_token_generator
# from django.contrib.auth import get_user_model

# from rest_framework import viewsets, status, filters
# from rest_framework import generics, mixins, views
# from rest_framework.mixins import CreateModelMixin, ListModelMixin
# from rest_framework.generics import ListAPIView


# from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.decorators import action


# # from api_yamdb.settings import PROJECT_MAIL

# from .serializers import (
#     UserSerializer, UserAuthSerializer, UserTokenSerializer,
#     FollowSerializer, TagSerializer,
#     RecipeSerializer, IngredientSerializer
# )
# from .permissions import (AdminRoleOnly, ReadOnly,
#                           IsAuthorModeratorAdminOrReadOnly)
# from foodgram.models import Recipe, Ingredient, Follow, Tag, Recipe
# from api.filters import TitleFilter


# User = get_user_model()


# class UserViewSet(viewsets.ModelViewSet):
#     """Класс-вьюсет для модели User."""
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (AdminRoleOnly,)
#     lookup_field = 'username'
#     filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
#     search_fields = ('username',)

#     @action(
#         detail=False,
#         url_path='me',
#         methods=['get', 'patch'],
#         permission_classes=[IsAuthenticated]
#     )
#     def handling_personal_info(self, request):

#         user = request.user

#         if request.method == 'PATCH':
#             serializer = UserSerializer(user, data=request.data, partial=True)
#             serializer.is_valid(raise_exception=True)
#             if user.role != User.USER:
#                 serializer.save()
#             else:
#                 serializer.save(role=user.role)
#         else:
#             serializer = UserSerializer(user)

#         return Response(serializer.data)


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def signup(request):
#     """View-функция для регистрации новых пользователей."""
#     serializer = UserAuthSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         user = get_object_or_404(
#             User, username=serializer.validated_data['username']
#         )
#         token = default_token_generator.make_token(user)
#         send_mail(
#             'Код подтверждения',
#             'Ваш код подтверждения: <{}>'.format(token),
#             PROJECT_MAIL,
#             [serializer.validated_data['email']],
#             fail_silently=False,
#         )
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def token_emission(request):
#     """View-функция для выдачи токена пользователю."""
#     serializer = UserTokenSerializer(data=request.data)
#     if serializer.is_valid():
#         user = get_object_or_404(
#             User,
#             username=serializer.validated_data['username']
#         )
#         refresh = RefreshToken.for_user(user)
#         return Response(
#             {'token': str(refresh.access_token)}, status=status.HTTP_200_OK
#         )
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# class RecipeViewSet(viewsets.ModelViewSet):
#     """View-функция для произведений."""
#     queryset = Recipe.objects.order_by('-id').annotate(
#         rating=Avg('reviews__score')
#     )
#     serializer_class = RecipeSerializer
#     permission_classes = [AdminRoleOnly | ReadOnly]
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = RecipeFilter


# class TagViewSet(viewsets.ReadOnlyModelViewSet):
#     """View-функция для категорий."""
#     queryset = Tag.objects.all()
#     serializer_class = TagSerializer
#     permission_classes = [AllowAny]
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['=name']
#     # lookup_field = 'id'



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


# # class IngredientViewSet(ListAPIView):
# class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
#     """View-функция для ингридиентов."""
#     queryset = Ingredient.objects.all()
#     serializer_class = IngredientSerializer
#     permission_classes = [AllowAny]
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['=name']
#     lookup_field = 'id'
