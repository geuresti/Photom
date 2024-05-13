from django.urls import path
from . import views
from .views import views_classes
from .views import views_students

from django.contrib.auth import views as auth_views

# /photomanager/...
urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("search_students/", views.search_students, name="search_students"),

   # path('reset_password/', 
   #     auth_views.PasswordResetView.as_view(
   #         template_name="registration/password_reset.html",
            #html_email_template_name="registration/email_template.html"
   #         ),
   #     name="reset_password"),

   # path('reset_password_sent/', 
   #     auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_sent.html"), 
   #     name="password_reset_done"),

   # path('reset/<uidb64>/<token>/',
   #     auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_form.html"),
   #     name="password_reset_confirm"),

   # path('reset_password_complete/',
   #     auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_done.html"),
   #     name="password_reset_complete"),

    path("hide_notification/<int:notif_id>/", views.hide_notification, name="hide_notification"),
    path("read_notification/<int:notif_id>/", views.read_notification, name="read_notification"),
    path("reset_notifications/", views.reset_notifications, name="reset_notifications"),

    path("account_settings/", views.account_settings, name="account_settings"),
    path("delete_account/", views.delete_account, name="delete_account"),

    path("manage_classes/", views_classes.manage_classes, name="manage_classes"),
    path("class_settings/<int:class_id>/", views_classes.class_settings, name="class_settings"),
    path("delete_class/<int:class_id>/", views_classes.delete_class, name="delete_class"),

    path("view_student/<int:student_id>/", views_students.view_student, name="view_student"),
    path("student_settings/<int:student_id>/", views_students.student_settings, name="student_settings"),
    path("delete_student/<int:student_id>/", views_students.delete_student, name="delete_student"),
    path("download_photo/<int:photo_id>/", views_students.download_photo, name="download_photo"),
]
