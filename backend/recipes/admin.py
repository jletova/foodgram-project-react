from django.contrib import admin

from .models import Recipe, User, IngredientInRecipe, Ingredient, Tag


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email', 'first_name', 'last_name', 'password'
    )
    search_fields = (
        'username', 'email', 'first_name', 'last_name'
    )


admin.site.register(User, UserAdmin)


class IngredientInRecipeInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientInRecipeInline,)
    list_display = (
        'author', 'name', 'text', 'image', 'cooking_time', 'tags'
    )
    search_fields = ('author', 'name', 'text', 'tags')
    # list_filter = ('author', 'cooking_time')


admin.site.register(Recipe, RecipeAdmin)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name', 'measurement_unit')


admin.site.register(Ingredient, IngredientAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'color', 'slug')


admin.site.register(Tag, TagAdmin)
