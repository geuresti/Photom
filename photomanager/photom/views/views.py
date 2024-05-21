from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from photom.models import SchoolAccount, Class, Student, SchoolAccount, Photo, Notification
from photom.forms import AccountForm, AccountSettingsForm
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

########################## GENERAL ##########################

def organize_classes(school):
    filetered_classes = Class.objects.filter(class_school=school).order_by("-class_grade")
    classes_a = [cls for cls in filetered_classes if cls.class_grade.isnumeric()]
    classes_b = [cls for cls in filetered_classes if not cls.class_grade.isnumeric()]
    classes_b.reverse()

    classes = classes_a + classes_b

    return classes

@login_required
def index(request):
    school = SchoolAccount.objects.get(user=request.user)

    classes = organize_classes(school)

    notifications = Notification.objects.filter(school=school, hidden=False)

    context = {
        "notifications":notifications,
        "classes":classes,
        "school":school
    }

    return render(request, "photom/index.html", context)

@login_required
def hide_notification(request, notif_id):

    notif = get_object_or_404(Notification, pk=notif_id)

    if not belongs_to_authenticated_user(request.user, notif.pk, 'notification'):
        return HttpResponseRedirect(reverse("index"))
    
    notif.hidden = True
    notif.read = True
    notif.save()

    print("\n HIDE NOTIFICATION #", notif_id, "\n")

    return HttpResponse(notif)

@login_required
def read_notification(request, notif_id):

    notif = get_object_or_404(Notification, pk=notif_id)

    if not belongs_to_authenticated_user(request.user, notif.pk, 'notification'):
        return HttpResponseRedirect(reverse("index"))
    
    notif.read = True
    notif.save()

    print("\n READ NOTIFICATION #", notif_id, "\n")

    return HttpResponse(notif)


# FOR TESTING THE INBOX
def reset_notifications(request):
    notifs = Notification.objects.all()

    for notif in notifs:
        notif.hidden = False
        notif.read = False
        notif.save()

    return HttpResponseRedirect(reverse("index"))

@login_required
def account_settings(request):

    school = SchoolAccount.objects.get(user=request.user)
    account_form = AccountForm()

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

@login_required
def search_students(request):

    school = SchoolAccount.objects.get(user=request.user)

    context = {
        "school":school,
    }

    if request.method == "POST":

        searched = request.POST['searched']
        context['searched'] = searched

        search_results = []

        classes = school.class_set.all()

        if searched.isnumeric():
            #print("\n ID SEARCHED \n")

            for cls in classes:
                students_by_id = cls.student_set.filter(student_ID__contains=searched)

                for student in students_by_id:
                    search_results.append(student)

            context['search_results'] = search_results

            return render(request, "photom/search_students.html", context)

        else:
            searched = searched.capitalize()

            # Filter each student of each class by the searched word
            for cls in classes:
                students_by_name = cls.student_set.filter(first_name__contains=searched) | cls.student_set.filter(last_name__contains=searched)

                for student in students_by_name:
                    if student not in search_results:
                        search_results.append(student)

            #print("\n search results:", search_results, "\n")

            context['search_results'] = search_results

            return render(request, "photom/search_students.html", context)
    else:

        return render(request, "photom/search_students.html", context)

########################## HELPER FUNCTION ##########################

# Helper function that checks if the associated object
# belongs to the authenticated user

# OR RETURN TRUE IF USER IS SUPERUSER
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
        classes = school.class_set.all()

        for cls in classes:
            students = cls.student_set.all()
            for student in students:
                if photo.student == student:
                    print("\n SUCCESS: PHOTO ACCESSED \n")
                    return True
            
        print("\n ERROR: THIS PHOTO DOES NOT BLEONG TO YOUR STUDENTS \n")
        return False
    
    elif association == 'notification':
        # Check if the photo belongs to the user
        notif = get_object_or_404(Notification, pk=pk)
        notifications = school.notification_set.all()

        if notif in notifications:
            print("\n SUCCESS: NOTIFICATION ACCESSED \n")
            return True
        else:
            print("\n ERROR: THIS NOTIFICATION DOES NOT BELONG TO YOU \n")
            return False
            
    else:
        return -1

########################## CREATE USER ##########################

def create_account(request):
    if request.method == "POST":

        account_form = AccountForm(request.POST)

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

        account_form = AccountForm()
        context = {
            "account_form":account_form,
        }

        return render(request, "registration/create_account.html", context)
    
@login_required
def account_settings(request):
    
    #school = SchoolAccount.objects.get(user=request.user)
    school = SchoolAccount.objects.get(user=request.user)

    if request.method == "POST":

        #account_form = AccountForm(request.POST, instance=school)
        account_form = AccountSettingsForm(request.POST)

        if account_form.is_valid():

            # Update database object
            print("\n ACCOUNT FORM VALID \n")

            account_form.save()

            return HttpResponseRedirect(reverse("manage_classes"))
        
        else:

            print("\n ACCOUNT FORM INVALID \n")

    account_form = AccountSettingsForm({
        "primary_key": school.pk,
        "first_name": school.user.first_name,
        "last_name": school.user.last_name,
        "username": school.user.username,
        "school_name": school.school_name,
        "school_phone": school.school_phone,
        "email": school.user.email,
        "school_position": school.school_position
    })

    context = {
        "account_form": account_form,
        "school": school
    }

    return render(request, "photom/account_settings.html", context)

@login_required
def delete_account(request):
    school_account = get_object_or_404(SchoolAccount, user=request.user)
    #school_account.delete()

    # Note: users might still be able to log in.
    #school_account.user.is_active = False
   # school_account.user.save()
    
    print("\n ACCOUNT SUCCESSFULLY DEACTIVATED (DISABLED) \n")

    return HttpResponseRedirect(reverse("login"))

@login_required
def delete_student(request, student_id):

    # Redirect if user attempting to delete a student from a different school
    if not belongs_to_authenticated_user(request.user, student_id, 'student'):
        return HttpResponseRedirect(reverse("index"))
    
    student_instance = get_object_or_404(Student, pk=student_id)
    student_instance.delete()
    print("\n STUDENT SUCCESSFULLY DELETED \n")

    return HttpResponseRedirect(reverse("manage_classes"))