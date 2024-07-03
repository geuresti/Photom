from django.shortcuts import render
from photom.models import Class, SchoolAccount, Notification
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from photom.forms import ClassForm, StudentForm
from django.contrib.auth.decorators import login_required
from .views import belongs_to_authenticated_user, organize_classes


# This view allows users to create students, create classes,
# and view a list of all their classes and the students within
@login_required
def manage_classes(request):

    # Get school of authenticated user
    school = SchoolAccount.objects.get(user=request.user)
    notifications = Notification.objects.filter(school=school, hidden=False)

    # Organize classes (by order of grade descending)
    classes = organize_classes(school)

    if request.method == "POST":

        # If the user submits a new class form
        if "create-class" in dict(request.POST.items()).keys():

            # add POST data into form object
            class_form = ClassForm(request.POST)

            if class_form.is_valid():
                print("\n CLASS FORM VALID \n")

                # Populate new form and save
                new_class = Class()
                new_class.class_name = class_form.data['class_name']
                new_class.class_teacher = class_form.data['class_teacher']
                new_class.class_grade = class_form.data['class_grade']
                new_class.class_school = school

                new_class.save()

                return HttpResponseRedirect(reverse("manage_classes"))
            else:
                print("\n ERROR: CLASS FORM INVALID \n")

        # If the user submits a new student form
        elif "create-student" in dict(request.POST.items()).keys():
            student_form = StudentForm(request.POST, request.FILES, user=request.user)

            # Check if the user selected a class before submitting
            if student_form.data['student_class'] == '-1':

                class_form = ClassForm()

                context = {
                    "class_form": class_form,
                    "student_form": student_form,
                    "classes": classes,
                    "school": school,
                    "notifications": notifications,
                    "select_error":True
                }

                return render(request, "photom/manage_classes.html", context)

            elif student_form.is_valid():
                print("\n STUDENT FORM VALID \n")
                student_form.save()    
                return HttpResponseRedirect(reverse("manage_classes"))
            else:
                print("\n ERROR: STUDENT FORM INVALID \n")
    else:
        class_form = ClassForm()

        # Pass the user to the form, this allows me to limit the class
        # dropdown options to classes belonging to the user's school
        student_form = StudentForm(user=request.user)

        context = {
            "class_form": class_form,
            "student_form": student_form,
            "classes": classes,
            "school": school,
            "notifications": notifications
        }

        return render(request, "photom/manage_classes.html", context)
    
# This view lets the user adjust the fields of the selected class
@login_required
def class_settings(request, class_id):
    class_instance = get_object_or_404(Class, pk=class_id)
    school = SchoolAccount.objects.get(user=request.user)
    
    # Redirect user if accessing the settings of a class that is not theirs
    if not belongs_to_authenticated_user(request.user, class_id, 'class'):
        return HttpResponseRedirect(reverse("index"))

    if request.method == "POST":

        class_form = ClassForm(request.POST, instance=class_instance)

        if class_form.is_valid():

            # Update database object
            print("\n CLASS FORM VALID \n")

            class_instance.class_name = class_form.data['class_name']
            class_instance.class_teacher = class_form.data['class_teacher']
            class_instance.class_grade = class_form.data['class_grade']
            class_instance.class_school = school

            class_instance.save()

            return HttpResponseRedirect(reverse("manage_classes"))
    else:
        # Populate the form with the current class field values
        class_form = ClassForm(instance=class_instance)

        context = {
            "class": class_instance,
            "class_form": class_form,
            "school": school
        }

        return render(request, "photom/class_settings.html", context)

# This view deletes the class using the given id  
@login_required
def delete_class(request, class_id):
    
    print("\n DELETE CLASS CALELD \n")

    class_instance = get_object_or_404(Class, pk=class_id)

    # Redirect if user attempting to delete class that isn't theirs
    if not belongs_to_authenticated_user(request.user, class_id, 'class'):
        return HttpResponseRedirect(reverse("index"))

    print("\n CLASS ID", class_id, "HAS BEING DELETED \n")
    class_instance.delete()

    return HttpResponseRedirect(reverse("manage_classes"))