from django.contrib import admin
from django.urls import include, path
from photom.views import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("photom/", include("photom.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/create_account/", views.create_account, name="create_account"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
