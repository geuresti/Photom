from django.contrib import admin
from django.urls import include, path
from photom.views import views

urlpatterns = [
    path("photom/", include("photom.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/create_account", views.create_account, name="create_account"),
]