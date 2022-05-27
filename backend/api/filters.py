from django_filters.rest_framework import (BooleanFilter, FilterSet,
                                           ModelMultipleChoiceFilter)

from .models import Recipe, Tag


class CustomFilter(FilterSet):
    tags = ModelMultipleChoiceFilter(
            field_name = 'tags__slug',
            to_field_name='slug',
            queryset=Tag.objects.all()
        )
    is_in_shopping_cart = BooleanFilter(method='filter_is_in_shopping_cart')
    is_favorited = BooleanFilter(method='filter_is_favorited')

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value == int(True) and user.is_authenticated:
            return queryset.filter(favouriterecipe__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value == int(True) and user.is_authenticated:
            return queryset.filter(shopping_cart__user=user)
        return queryset
        

    class Meta:
        model = Recipe
        fields = ('tags', 'author')
 