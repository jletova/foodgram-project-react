from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AddDeleteFollowViewSet, TagViewSet,
                    FollowViewSet, RecipeViewSet)

router = DefaultRouter()
# router.register(
#     r'posts/(?P<post_id>\d+)/comments',
#     CommentViewSet,
#     basename="comments"
# )
router.register(r'tags', TagViewSet, basename="tags")
router.register(r'recipes', RecipeViewSet, basename="recipes")
# router.register(r'follow', FollowViewSet, basename="follows")
router.register(r'subscriptions', FollowViewSet, basename="follows")
router.register(
    r'(?P<user_id>\d+)/subscribe',
    AddDeleteFollowViewSet,
    basename="add_delete_follow"
)

urlpatterns = [
    path(r'^users/', include('djoser.urls')),
    path(r'^users/', include('djoser.urls.authtoken')),
    path(r'^users/', include(router.urls)),


]
