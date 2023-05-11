from django import forms

from .models import Category, JarItem


class TodoItemForm(forms.ModelForm):
    class Meta:
        model = JarItem
        fields = ["name"]


class DoneItemForm(forms.ModelForm):
    class Meta:
        model = JarItem
        fields = ["name", "done_date"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ["name", "todo_verb", "done_verb"]
