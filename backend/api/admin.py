from django.contrib import admin

from .models import (FavouriteRecipe, Follow, Ingredient, IsInShoppingCart,
                     Recipe, Tag, User)


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'password'
    )
    search_fields = (
        'username', 'email', 'first_name', 'last_name'
    )
    list_filter = ('email', 'first_name')


admin.site.register(User, UserAdmin)


class IngredientsAmountInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class TagsInRecipeInline(admin.TabularInline):
    model = Recipe.tags.through
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientsAmountInline, )
    list_display = ('name', 'author', 'id')
    search_fields = ('author', 'name', 'text', 'tags')
    list_filter = ('author', 'name', 'tags')


admin.site.register(Recipe, RecipeAdmin)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit', 'id')
    search_fields = ('name', 'measurement_unit')
    list_filter = ('name',)


admin.site.register(Ingredient, IngredientAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'color', 'slug')


admin.site.register(Tag, TagAdmin)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')
    search_fields = ('user', 'following')


admin.site.register(Follow, FollowAdmin)


class FavouriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user', 'recipe')


admin.site.register(FavouriteRecipe, FavouriteRecipeAdmin)


class IsInShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'id')
    search_fields = ('user', 'recipe')


admin.site.register(IsInShoppingCart, IsInShoppingCartAdmin)
