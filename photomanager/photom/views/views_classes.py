from django.shortcuts import render
from photom.models import Class, SchoolAccount
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from photom.forms import ClassForm, StudentForm
from django.contrib.auth.decorators import login_required

# CLASS MUST BELONG TO THE USER
@login_required
def manage_classes(request):

    school = SchoolAccount.objects.get(user=request.user)
    classes = Class.objects.filter(class_school = school).order_by("-class_grade")
    print("\n CLASSES: ", classes, "\n")

    if request.method == "POST":

        if "create-class" in dict(request.POST.items()).keys():
            # add POST data into form object
            class_form = ClassForm(request.POST)

            if class_form.is_valid():
                print("\n CLASS FORM VALID \n")

                new_class = Class()
                new_class.class_name = class_form.data['class_name']
                new_class.class_teacher = class_form.data['class_teacher']
                new_class.class_grade = class_form.data['class_grade']
                new_class.class_school = school

                new_class.save()

                return HttpResponseRedirect(reverse("manage_classes"))
            else:
                print("\n CLASS FORM INVALID \n")

        elif "create-student" in dict(request.POST.items()).keys():
            student_form = StudentForm(request.POST, request.FILES)

            print("\n STUDENT DATa: ", student_form.data, "\n")

            if student_form.data['student_class'] == '-1':
                print("\n STUDENT FORM NOTHING WAS SELECTED NOW WHAT? \n")

                class_form = ClassForm()

                context = {
                    "class_form": class_form,
                    "student_form": student_form,
                    "classes":classes,
                    "school":school,
                    "select_error":True
                }

                return render(request, "photom/manage_classes.html", context)

            elif student_form.is_valid():
                print("\n STUDENT FORM VALID \n")
                student_form.save()    

                return HttpResponseRedirect(reverse("manage_classes"))
            else:
                print("\n STUDENT FORM INVALID \n")
    else:
        class_form = ClassForm()
        student_form = StudentForm()

        context = {
            "class_form": class_form,
            "student_form": student_form,
            "classes":classes,
            "school":school
        }

        return render(request, "photom/manage_classes.html", context)
    
# CLASS MUST BELONG TO THE USER
@login_required
def class_settings(request, class_id):

    class_instance = get_object_or_404(Class, pk=class_id)
    school = SchoolAccount.objects.get(user=request.user)

    # Redirect user if accessing the settings of a class that is not theirs
    if class_instance not in school.class_set.all():
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
        class_form = ClassForm(instance=class_instance)

        context = {
            "class": class_instance,
            "class_form": class_form
        }

        return render(request, "photom/class_settings.html", context)
    
# CLASS MUST BELONG TO THE USER
def delete_class(request, class_id):

    class_instance = get_object_or_404(Class, pk=class_id)
    class_instance.delete()

    return HttpResponseRedirect(reverse("manage_classes"))