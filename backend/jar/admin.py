from django.contrib import admin

from .models import Category, JarItem


class JarItemInline(admin.TabularInline):
    model = JarItem
    prepopulated_fields = {"slug": ("name",)}
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [JarItemInline]
