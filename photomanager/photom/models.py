from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Has not been migrated
#class PhotographerAccount(models.Model):
 #   user = models.OneToOneField(User, on_delete=models.CASCADE)

  #  def __str__(self):
   #     return self.user.first_name + ", " + self.user.last_name
    
class SchoolAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school_phone = PhoneNumberField(region="US")
    school_name = models.CharField(max_length=100)
    school_position = models.CharField(max_length=100)

    def __str__(self):
        return self.school_name

class Photo(models.Model):
    photo = models.ImageField(upload_to="student-pictures")
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    school_account = models.ForeignKey("SchoolAccount", on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True, blank=True)

"""
STUDENT DATA 

(OPTIONAL) photo id
Age *
ID Number
Student Last Name
Student First Name
Homeroom Teacher
"""
class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    student_age = models.IntegerField()
    student_class = models.ForeignKey("Class", on_delete=models.CASCADE)
    student_ID = models.IntegerField()
    student_photo_ID = models.ImageField(default="photo-ids/default-photo-id.PNG", upload_to="photo-ids")

    def __str__(self):
        return self.first_name + " " + self.last_name

"""
CLASS DATA

Grade (can be “KG” or “PK”) (UPDATE TO CHAR FIELD)
"""
class Class(models.Model):
    class_name = models.CharField(max_length=50)
    class_teacher = models.CharField(max_length=50)
    class_grade = models.IntegerField()
    # CLASS_GRADE needs to be a charfield because grade "PK" and "KG"
    class_grade = models.IntegerField()

    class_school = models.ForeignKey(SchoolAccount, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.class_name