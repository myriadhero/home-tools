from django.urls import path

from .views import (
    ChosenItemDoneView,
    ItemChooseRandomView,
    ItemChooseView,
    ItemCreateView,
    ItemDeleteView,
    ItemDoneView,
    ItemEditView,
    ItemGetView,
    JarRedirect,
    SingleJarView,
)

app_name = "jar"
urlpatterns = [
    path("", JarRedirect.as_view(), name="jars"),
    path("c/<slug:category>", SingleJarView.as_view(), name="jar"),
    path(
        "c/<slug:category>/create",
        ItemCreateView.as_view(),
        name="item_create",
    ),
    path(
        "c/<slug:category>/choose",
        ItemChooseRandomView.as_view(),
        name="item_choose_random",
    ),
    path(
        "c/<slug:category>/done",
        ChosenItemDoneView.as_view(),
        name="chosen_item_done",
    ),
    path(
        "i/<int:item>",
        ItemGetView.as_view(),
        name="item_get",
    ),
    path(
        "i/<int:item>/done",
        ItemDoneView.as_view(),
        name="item_done",
    ),
    path(
        "i/<int:item>/choose",
        ItemChooseView.as_view(),
        name="item_choose",
    ),
    path(
        "i/<int:item>/delete",
        ItemDeleteView.as_view(),
        name="item_delete",
    ),
    path(
        "i/<int:item>/edit",
        ItemEditView.as_view(),
        name="item_edit",
    ),
]
