from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.db import models
from photomanager import settings
import os

class SchoolAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school_phone = PhoneNumberField(region="US")
    school_name = models.CharField(max_length=100)
    school_position = models.CharField(max_length=100)
    has_csv = models.BooleanField(default=False)

    def __str__(self):
        return self.school_name
    
    class Meta:
        verbose_name = "School"
        verbose_name_plural = "Schools"
    
class Notification(models.Model):
    title = models.CharField(max_length=50)
    message = models.CharField(max_length=150)
    date_sent = models.DateTimeField(auto_now_add=True, blank=True)
    read = models.BooleanField(default=False, blank=True)
    hidden = models.BooleanField(default=False, blank=True)
    school = models.ForeignKey(SchoolAccount, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Class(models.Model):
    class_name = models.CharField(max_length=50)
    class_teacher = models.CharField(max_length=50)
    class_grade = models.CharField(max_length=50)
    class_school = models.ForeignKey(SchoolAccount, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return "(" + str(self.class_school) + ") " + self.class_name
    
    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    student_class = models.ForeignKey("Class", on_delete=models.CASCADE)
    student_ID = models.IntegerField()
    student_photo_ID = models.ImageField(default="photo-ids/default-photo-id.PNG", upload_to="photo-ids")

    def __str__(self):
        return self.first_name + " " + self.last_name  + " #" + str(self.student_ID)
    
    def delete(self, *args, **kwargs):
    
        # Delete student's photo ID
        if self.student_photo_ID and str(self.student_photo_ID) != 'photo-ids/default-photo-id.PNG':
            os.remove(os.path.join(settings.MEDIA_ROOT, str(self.student_photo_ID)))
            self.student_photo_ID = ""
            self.save()

        # Delete all of this student's photos
        photos = Photo.objects.filter(student=self)
        for photo in photos:
            os.remove(os.path.join(settings.MEDIA_ROOT, str(photo.photo)))
            photo.delete()

        super(Student, self).delete(*args,**kwargs)

class Photo(models.Model):
    photo = models.ImageField(upload_to="student-pictures")
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True, blank=True)

    # Helper functions for admin dashboard
    def preview(self):
        return format_html('<img href="{0}" src="{0}" width="50" height="50" />'.format(self.photo.url))

    def picture(self):
        return format_html('<img href="{0}" src="{0}" width="150" height="150" />'.format(self.photo.url))

    def __str__(self):
        string = str(self.photo).split("/")[1]
        return string