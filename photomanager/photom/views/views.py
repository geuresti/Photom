from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from photom.models import Class, Student, SchoolAccount, Photo
from photom.forms import AccountCreationForm  
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

########################## GENERAL ##########################

@login_required
def index(request):
    school = SchoolAccount.objects.get(user=request.user)
    classes = Class.objects.filter(class_school = school).order_by("-class_grade")

    context = {
        "classes":classes,
        "school":school
    }

    return render(request, "photom/index.html", context)

@login_required
def admin_view(request):
    # If user is superuser, render page
    # Else, redirect to home page
    response = "You're looking at the admin dashboard"
    return HttpResponse(response)

@login_required
def account_settings(request):

    school = SchoolAccount.objects.get(user=request.user)
    account_form = AccountCreationForm()

    context = {
        "school":school,
        "account_form":account_form
    }

    return render(request, "photom/account_settings.html", context)

@login_required
def about(request):
    school = SchoolAccount.objects.get(user=request.user)
    context = {
        'school': school
    }
    return render(request, "photom/about.html", context)

@login_required
def contact(request):
    school = SchoolAccount.objects.get(user=request.user)
    context = {
        'school': school
    }
    return render(request, "photom/contact.html", context)

# Helper function that checks if the associated object
# belongs to the authenticated user
def belongs_to_authenticated_user(user, pk, association):
    school = SchoolAccount.objects.get(user=user)

    if association == 'class':
        class_instance = get_object_or_404(Class, pk=pk)

        # Check if class belongs to the user
        if class_instance not in school.class_set.all():
            print("\n ERROR: THIS CLASS DOES NOT BLEONG TO YOU \n")
            return False
        else:
            print("\n SUCCESS: CLASS ACCESSED \n")
            return True
    elif association == 'student':
        # Check if student belongs to the user
        student_instance = get_object_or_404(Student, pk=pk)
        student_class = get_object_or_404(Class, pk=student_instance.student_class_id)

        if student_class not in school.class_set.all():
            print("\n ERROR: THIS STUDENT IS NOT IN YOUR CLASSES \n")
            return False
        else:
            print("\n SUCCESS: STUDENT ACCESSED \n")
            return True
    elif association == 'photo-id':
        # Check if the photo belongs to the user
        photo = get_object_or_404(Photo, pk=pk)
        if photo.school_account != school:
            print("\n ERROR: THIS PHOTO DOES NOT BLEONG TO YOUR STUDENTS \n")
            return False
        else:
            print("\n SUCCESS: PHOTO ACCESSED \n")
            return True
    else:
        return -1

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
