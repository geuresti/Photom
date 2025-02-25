from django.urls import path
from django.contrib.auth import views as auth_views
from photom.forms import CustomPasswordResetForm, CustomEmailPasswordResetForm
from .views import views_classes, views_students
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    # Download files
    path("download_school_photos/<int:pk>/", views.download_school_photos, name="download_school_photos"),
    path("download_class_photos/<int:pk>/", views.download_class_photos, name="download_class_photos"),
    path("download_school_csv/<int:pk>/", views.download_school_csv, name="download_school_csv"),
    path("download_photo/<int:photo_id>/", views_students.download_photo, name="download_photo"),

    # General views
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("schools_dashboard/", views.schools_dashboard, name="schools_dashboard"),
    path("search_students/", views.search_students, name="search_students"),
    
    # Password reset
    path('password_reset/', 
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset.html",
            html_email_template_name="registration/email_template.html",
            form_class=CustomEmailPasswordResetForm
        ),
        name="photom_password_reset"),
    
    path('password_reset_done/', 
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ), 
        name="photom_password_reset_done"),

    path('password_reset_confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
           template_name="registration/password_reset_confirm.html",
           form_class=CustomPasswordResetForm,
        ),
        name="photom_password_reset_confirm"),

    path('password_reset_complete/',
        auth_views.PasswordResetCompleteView.as_view(
           template_name="registration/password_reset_complete.html"
        ),
        name="photom_password_reset_complete"),

    # Notifications
    path("notifications", views.notifications, name="notifications"),
    path("hide_notification/<int:notif_id>/", views.hide_notification, name="hide_notification"),
    path("read_notification/<int:notif_id>/", views.read_notification, name="read_notification"),
        # path("reset_notifications/", views.reset_notifications, name="reset_notifications"),

    # Manage account
    path("account_settings/", views.account_settings, name="account_settings"),
    path("delete_account/", views.delete_account, name="delete_account"),

    # Manage class
    path("manage_classes/", views_classes.manage_classes, name="manage_classes"),
    path("class_settings/<int:class_id>/", views_classes.class_settings, name="class_settings"),
    path("delete_class/<int:class_id>/", views_classes.delete_class, name="delete_class"),

    # Upload files
    path("upload_student_data/", views_students.upload_csv, name="upload_csv"),
    path("read_student_data/", views_students.read_students_csv, name="read_students_csv"),
    path("upload_photos/", views_students.FileFieldFormView.as_view(), name="upload_photos"),
    path("upload_photos/success", views_students.reset_image_upload, name="upload_photos_success"),

    # Manage student
        #path("view_student/<int:student_id>/", views_students.view_student, name="view_student"),
    path("student_settings/<int:student_id>/", views_students.student_settings, name="student_settings"),
    path("delete_student/<int:student_id>/", views_students.delete_student, name="delete_student"),
]