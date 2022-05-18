from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TagViewSet, IngredientViewSet, RecipeViewSet
# , AddDeleteFollowViewSet, 
                    # FollowViewSet, RecipeViewSet)


router = DefaultRouter()

router.register(r'tags', TagViewSet, basename="tags")
router.register(r'ingredients', IngredientViewSet, basename="ingredients")

router.register(r'recipes', RecipeViewSet, basename="recipes")


# # router.register(r'follow', FollowViewSet, basename="follows")
# router.register(r'subscriptions', FollowViewSet, basename="subscriptions")
# router.register(
#     r'(?P<user_id>\d+)/subscribe',
#     AddDeleteFollowViewSet,
#     basename="add_delete_follow"
# )


urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),

]

