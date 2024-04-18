"""
ORIGINAL IMPORTS

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .models import Student, Class
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import ClassForm, StudentForm, UploadFileForm
from views.views_classes import *
"""

from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from photom.models import Student, Class
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from photom.forms import AccountCreationForm  
from django.http import HttpResponseRedirect

########################## GENERAL ##########################

# order dropdown
# USER MUST BE LOGGED IN
def index(request):
    classes = Class.objects.all().order_by("-class_grade")
    context = {
        "classes":classes,
    }
    return render(request, "photom/index.html", context)

def admin_view(request):
    # If user is superuser, render page
    # Else, redirect to home page
    response = "You're looking at the admin dashboard"
    return HttpResponse(response)

def account_settings(request):

    response = "Here is the account settings page"
    return HttpResponse(response)

########################## CREATE USER ##########################

def create_account(request):
    if request.method == "POST":

        account_form = AccountCreationForm(request.POST)

        if account_form.is_valid():

            print("\n USER SUCCESSFULLY CREATED (disabled) \n")
            #user_form.save()
            return HttpResponseRedirect("/login/")
            #user.save()
        else:
            print("\n USER FORM INVALID (disabled) \n")

    else:

        account_form = AccountCreationForm()
        context = {
            "account_form":account_form,
        }

        return render(request, "registration/create_account.html", context)


########################## MISC ##########################

import PIL.Image as Image
import io
import base64

def test_image(request):
    student_instance = get_object_or_404(Student, pk=11)
    byte_data = student_instance.student_photo_ID_B
    b = base64.b64decode(byte_data)

    byteImgIO = io.BytesIO(b)
    byteImg = Image.open(byteImgIO)
    byteImg.save(byteImgIO, "PNG")
    byteImgIO.seek(0)
    byteImg = byteImgIO.read()

    dataBytesIO = io.BytesIO(byteImg)
    Image.open(dataBytesIO)

    context = {
        "image": byteImg
    }

    return render(request, "photom/test_template.html", context)
