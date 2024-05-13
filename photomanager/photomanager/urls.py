from django.contrib import admin
from django.urls import include, path
from photom.views import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("photom/", include("photom.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),

    path('accounts/reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name="photom/registration/password_reset_form.html"),
        name="password_reset_confirm"),

    path('accounts/reset_password/', 
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset.html",
            #html_email_template_name="registration/email_template.html"
            ),
        name="reset_password"),

    path('accounts/reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_sent.html"), 
        name="password_reset_done"),

    path('accounts/reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_done.html"),
        name="password_reset_complete"),

    path("accounts/create_account/", views.create_account, name="create_account"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#  I want to exclude some of the auth urls ?
