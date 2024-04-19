from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from photom.models import Class
from photom.forms import AccountCreationForm  
from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required

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

            print("\n USER SUCCESSFULLY CREATED \n")
            account_form.save()
            return HttpResponseRedirect("/accounts/login/")
        else:
            print("\n USER FORM INVALID \n")

            context = {
                "account_form":account_form,
            }

            return render(request, "registration/create_account.html", context)
    else:

        account_form = AccountCreationForm()
        context = {
            "account_form":account_form,
        }

        return render(request, "registration/create_account.html", context)
