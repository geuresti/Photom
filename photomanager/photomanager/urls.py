from django.contrib import admin
from django.urls import include, path
from photom.views import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from photom.forms import CustomLoginForm

urlpatterns = [
    path("photom/", include("photom.urls")),
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

# I want to exclude some of the auth urls ?
# overwrite before "include"
