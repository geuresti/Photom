from django import forms
from .models import Student, Class, Photo, SchoolAccount
from django.utils.translation import gettext as _

from django.contrib.auth.models import User  
from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField
from django.forms.fields import EmailField  
from django.forms.forms import Form  


class AccountCreationForm(UserCreationForm):  
    first_name = forms.CharField(label="fisrt name", min_length=1, max_length=100)
    last_name = forms.CharField(label="last name", min_length=1, max_length=100)
    school_phone = PhoneNumberField()
    school_name = forms.CharField(label="school name", max_length=200)
    school_position = forms.CharField(label="position at the school", max_length=100)
    username = forms.CharField(label='username', min_length=5, max_length=150)  
    email = forms.EmailField(label='email')  
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)  
  
    # Formatting? Region?
    #def phone_clean(self):
    #    return 

    # Formatting? Check for copy?
    # def school_clean(self):
    #    return 

    # Formatting?
    # def school_position(self):
    #   return

    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        already_exists = User.objects.filter(username=username)  
        if already_exists.count():  
            raise ValidationError("The username '", username, "' is already taken")
          
        return username  
  
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError("The email '", email, "' is already being used")
          
        return email  
  
    def password_clean(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("The passwords you entered do not match")  
        
        return password2  
  
    def save(self, commit=True):  
        user = User.objects.create_user( 
            self.cleaned_data['username'],
            self.cleaned_data['email'],  
            self.cleaned_data['password1']  
        )

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        school = SchoolAccount()
        school.user = user
        school.school_phone = self.cleaned_data['school_phone']
        school.school_name = self.cleaned_data['school_name']
        school.school_position = self.cleaned_data['school_position']
        school.save()

        return school

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ["class_name", "class_teacher", "class_grade"]
        labels = {
            "class_name": _("Class"),
            "class_teacher": _("Teacher"),
            "class_grade": _("Grade")
        }

class StudentForm(forms.ModelForm):

    student_photo_ID = forms.ImageField(required=False, error_messages = {'invalid':_("Image files only")}, widget=forms.FileInput)

    class Meta:
        model = Student
        fields = [
            "first_name", 
            "last_name", 
            "student_age",
            "student_class",
            "student_ID",
            "student_photo_ID",
        ]
        labels = {
            "first_name": _("First Name"),
            "last_name": _("Last Name"),
            "student_age": _("Age"),
            "student_class": _("Class"),
            "student_ID": _("ID #"),
            "student_photo_ID": _("Photo ID"),
        }

# Kind of useless as a model from since I have to manually set
# some values rather than just calling form.save()
class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = [
            "photo"
        ]
