from typing import Any, List, Optional

from django.http import HttpResponse, HttpResponseRedirect
from django.http.request import QueryDict
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import RedirectView, TemplateView

from .forms import DoneItemForm, TodoItemForm
from .models import Category, JarItem


# Create your views here.
class JarRedirect(RedirectView):
    permanent = False
    pattern_name = "jar:jar"

    def get_redirect_url(self, *args: Any, **kwargs: Any):
        first_category = Category.objects.first()
        return reverse(self.pattern_name, kwargs={"category":first_category.slug})

class SingleJarView(TemplateView):
    template_name = "jar/allJars.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["current_category"] = get_object_or_404(Category, slug=self.kwargs["category"])
        return context


class HTMXJarItemsView(TemplateView):
    template_name = "jar/singleJar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "category" in self.kwargs:
            category = self.get_category()
        else:
            item = self.get_jar_item()
            category = item.category
        context["category"] = category
        return context

    def get_jar_item(self) -> JarItem:
        return get_object_or_404(JarItem, pk=self.kwargs["item"])

    def get_category(self) -> Category:
        return get_object_or_404(Category, slug=self.kwargs["category"])


class ItemCreateView(HTMXJarItemsView):
    class_form = TodoItemForm
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        category = get_object_or_404(Category, slug=self.kwargs["category"])
        form = self.class_form(request.POST)

        if form.is_valid():
            item: JarItem = form.save(commit=False)
            item.category = category
            item.save()

        return self.get(request, *args, **kwargs)


class ItemChooseRandomView(HTMXJarItemsView):
    http_method_names = ["put"]

    def put(self, request, *args, **kwargs):
        category: Category = get_object_or_404(Category, slug=self.kwargs["category"])
        category.choose_random()

        return self.get(request, *args, **kwargs)


class ChosenItemDoneView(HTMXJarItemsView):
    http_method_names = ["put"]

    def put(self, request, *args, **kwargs):
        category: Category = get_object_or_404(Category, slug=self.kwargs["category"])
        category.make_chosen_done()

        return self.get(request, *args, **kwargs)


class ItemGetView(TemplateView):
    http_method_names = ["get", "patch"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item"] = get_object_or_404(JarItem, pk=self.kwargs["item"])
        return context

    def get_template_names(self) -> List[str]:
        item: JarItem = get_object_or_404(JarItem, pk=self.kwargs["item"])
        if item.is_done:
            return ["jar/includes/done_item.html"]
        return ["jar/includes/todo_item.html"]

    def patch(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class ItemChooseView(HTMXJarItemsView):
    http_method_names = ["put"]

    def put(self, request, *args, **kwargs):
        item = self.get_jar_item()
        item.choose()

        return self.get(request, *args, **kwargs)


class ItemDoneView(HTMXJarItemsView):
    http_method_names = ["put"]

    def put(self, request, *args, **kwargs):
        item = self.get_jar_item()
        item.toggle_done()

        return self.get(request, *args, **kwargs)


class ItemEditView(TemplateView):
    http_method_names = ["get", "patch"]

    def get_template_names(self) -> List[str]:
        item: JarItem = get_object_or_404(JarItem, pk=self.kwargs["item"])
        if item.is_done:
            return ["jar/forms/done_item_form.html"]
        return ["jar/forms/todo_item_form.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item"] = get_object_or_404(JarItem, pk=kwargs["item"])
        return context

    def patch(self, request, *args, **kwargs):
        item: JarItem = get_object_or_404(JarItem, pk=kwargs["item"])
        Form = DoneItemForm if item.is_done else TodoItemForm
        form = Form(QueryDict(request.body))

        if form.is_valid():
            new_item: JarItem = form.save(commit=False)
            item.name = new_item.name
            if item.is_done:
                item.done_date = new_item.done_date
            item.save()

        return redirect(
            reverse("jar:item_get", kwargs={"item": item.id}), permanent=False
        )


class ItemDeleteView(HTMXJarItemsView):
    http_method_names = ["delete"]

    def delete(self, request, *args, **kwargs):
        item = self.get_jar_item()
        category = item.category
        is_done = item.is_done
        self.kwargs["category"] = category.slug
        item.delete()
        content = ""
        if is_done:
            if not category.get_done().exists():
                content = f"Get something {category.done_verb.lower()}!"
        else:
            if not category.get_todo().exists():
                content = f"Add something {category.todo_verb.lower()}!"

        return HttpResponse(content)
