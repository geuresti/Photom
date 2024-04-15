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
  
    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username  
  
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError(" Email Already Exist")  
        return email  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  
  
  # *********
    def save(self, commit=True):  
        user = User.objects.create_user(  
            self.cleaned_data['username'],  
            self.cleaned_data['email'],  
            self.cleaned_data['password1']  
        )  
        return user  

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
