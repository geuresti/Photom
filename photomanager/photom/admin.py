from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Student, Class, Notification, SchoolAccount, Photo
from .forms import NotificationForm
from django.db import models

# Remove "Groups" "User Permissions" from 
# User edit page in admin dashboard
class UserAdmin(BaseUserAdmin):
    actions = None
    list_display = ['first_name', 'last_name', 'email']
    
    fieldsets = [
        ('User Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Account Info', {'fields': ('password', 'is_active')}),
        ('Authentication', {'fields': ('last_login', 'date_joined')}),
    ]

class SchoolAccountAdmin(admin.ModelAdmin):
    actions = None
    list_display = ['__str__', 'user', 'school_phone']
    exclude = ['school_position']
    readonly_fields = ['user']

    def has_add_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False

class ClassAdmin(admin.ModelAdmin):
    actions = None
    list_display = ['class_name', 'class_school', 'class_grade', 'class_teacher']
    list_display_links = ['class_name']
    ordering = ['class_school']
    search_fields = ['class_name', 'class_school__school_name']

class StudentAdmin(admin.ModelAdmin):
    actions = None
    list_display = ['last_name', 'first_name', 'student_ID', 'student_class']
    ordering = ['last_name']
    search_fields = ['last_name', 'first_name', 'student_ID']

class PhotoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': (('photo', 'picture'), 'student', 'upload_date')}),
    ]
    
    actions = None
    list_display = ['__str__', 'student', 'upload_date', 'preview']
    readonly_fields = ['upload_date', 'preview', 'picture']
    search_fields = ['student__last_name', 'student__first_name', 'student__student_ID']
    autocomplete_fields = ['student']
    list_per_page = 10

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'school', 'date_sent', 'read']
    exclude = ['hidden']
    readonly_fields = ['read', 'date_sent']
    ordering = ['-date_sent']
    search_fields = ['title', 'school__school_name']

    form = NotificationForm

    #formfield_overrides = {
#        models.TextField: {"widget": models.TextField},
   # }

admin.site.register(SchoolAccount, SchoolAccountAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Notification, NotificationAdmin)

admin.site.unregister(Group)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)