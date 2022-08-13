from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("layout",views.layout, name="layout"),
    path("create",views.create,name="create"),
    path("random",views.randompage,name="random"),
    path("editentry/<str:name>",views.editentry,name="editentry"),
    path("save",views.save,name="save"),
    path("search",views.search,name="search"),
    path("<str:name>", views.entry, name="entry")
]
