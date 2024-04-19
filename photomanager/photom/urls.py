from django.urls import path
from . import views
from .views import views_classes
from .views import views_students

# /photomanager/...
urlpatterns = [
    path("", views.index, name="index"),
    path("admin_view/", views.admin_view, name="admin_view"),
    path("account_settings/", views.account_settings, name="account_settings"),

    path("manage_classes/", views_classes.manage_classes, name="manage_classes"),
    path("class_settings/<int:class_id>/", views_classes.class_settings, name="class_settings"),
    path("delete_class/<int:class_id>/", views_classes.delete_class, name="delete_class"),

    path("view_student/<int:student_id>/", views_students.view_student, name="view_student"),
    path("student_settings/<int:student_id>/", views_students.student_settings, name="student_settings"),
    path("delete_student/<int:student_id>/", views_students.delete_student, name="delete_student"),
    path("download_photo/<int:photo_id>/", views_students.download_photo, name="download_photo"),
]
