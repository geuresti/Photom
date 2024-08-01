from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from photom.views import views, views_students
from photom.forms import CustomLoginForm

urlpatterns = [
    path("", views.index),
    path("photom/", include("photom.urls")),
    path("admin/upload_csv/", views_students.upload_csv),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/create_account/", views.create_account, name="create_account"),
    path("photom/login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=CustomLoginForm
            ),
        name="login"
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)