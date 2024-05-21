from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

from django.contrib import admin

class SchoolAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school_phone = PhoneNumberField(region="US")
    school_name = models.CharField(max_length=100)
    school_position = models.CharField(max_length=100)

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
    
"""
CLASS DATA

Class Name
Homeroom Teacher
Grade (can be “KG” or “PK”)
School
"""
class Class(models.Model):
    class_name = models.CharField(max_length=50)
    class_teacher = models.CharField(max_length=50)
    class_grade = models.CharField(max_length=50)
    class_school = models.ForeignKey(SchoolAccount, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return "(" + str(self.class_school) + ") " + self.class_name
       # return self.class_name        
    
    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
"""
STUDENT DATA 

(OPTIONAL) photo id
Age *
ID Number
Student Last Name
Student First Name
"""
class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    #student_age = models.IntegerField()
    student_class = models.ForeignKey("Class", on_delete=models.CASCADE)
    student_ID = models.IntegerField()
    student_photo_ID = models.ImageField(default="photo-ids/default-photo-id.PNG", upload_to="photo-ids")
    
  #  @admin.display(description="Student Pictures")
  #  def get_photos(self):
  #      photos = self.photo_set.all()
   #     print("\n GOT PHOTOS:", photos, "\n")
  #      return photos

    def __str__(self):
        return self.first_name + " " + self.last_name  + " #" + str(self.student_ID)

from django.utils.html import format_html

class Photo(models.Model):
    photo = models.ImageField(upload_to="student-pictures")
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True, blank=True)

    def preview(self):
        return format_html('<img href="{0}" src="{0}" width="50" height="50" />'.format(self.photo.url))

    def picture(self):
        return format_html('<img href="{0}" src="{0}" width="150" height="150" />'.format(self.photo.url))

    def __str__(self):
        string = str(self.photo).split("/")[1]
        return string