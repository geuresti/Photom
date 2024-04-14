from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

from django.core.files.storage import FileSystemStorage

# user model has:
# first name *
# last name *
# email *
# username
# password
# user permissions

class SchoolAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school_phone = PhoneNumberField(default="4155550132")
    school_name = models.CharField(max_length=200)
    school_position = models.CharField(max_length=100)

# student needs student_photo (is that what she meant by student id?)
# student needs photos
    
#fs = FileSystemStorage(location="/media/photo-ids")

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    student_age = models.IntegerField()
    student_class = models.ForeignKey("Class", on_delete=models.CASCADE)
    student_ID = models.IntegerField()
  #  student_photo_ID = models.ImageField(default="https://adonisrecycling.com/wp-content/uploads/2021/06/male-placeholder.jpeg", upload_to="photo-ids") #, storage=fs, upload_to="")
    student_photo_ID = models.ImageField(upload_to="photo-ids") #, storage=fs, upload_to="")
   # student_photo_ID = models.FileField(default="https://adonisrecycling.com/wp-content/uploads/2021/06/male-placeholder.jpeg", blank=True)

    student_photos = ArrayField(models.CharField(max_length=200), default=[], blank=True, null=True)

    def __str__(self):
        return self.first_name + ", " + self.last_name # + ", " + str(self.student_age) + ", " + str(self.student_class) + ", " + str(self.student_ID)
    
class Class(models.Model):
    class_name = models.CharField(max_length=50)
    class_teacher = models.CharField(max_length=50)
    class_grade = models.IntegerField()

    def __str__(self):
        return self.class_name