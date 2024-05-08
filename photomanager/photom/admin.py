from django.contrib import admin
from .models import Student, Class, Notification, SchoolAccount, Photo

admin.site.register(SchoolAccount)
admin.site.register(Class)
admin.site.register(Student)
admin.site.register(Photo)
admin.site.register(Notification)