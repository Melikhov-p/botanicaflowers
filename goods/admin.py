from django.contrib import admin

from goods.models import Category, Product, Like


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount_percent', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('discount_percent',)
    list_filter = ('name',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount_percent', 'amount', 'available',)
    list_filter = ('available', 'category')
    list_editable = ('price', 'discount_percent', 'amount', 'available',)


class LikeAdmin(admin.ModelAdmin):
    list_display = ('product', 'client',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Like, LikeAdmin)
