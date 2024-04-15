from django.shortcuts import render
from photom.models import Class
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from photom.forms import ClassForm, StudentForm

# CLASS MUST BELONG TO THE USER
def manage_classes(request):

    if request.method == "POST":

        if "create-class" in dict(request.POST.items()).keys():
            # add data into form object
            class_form = ClassForm(request.POST)

            if class_form.is_valid():
                class_form.save()
                return HttpResponseRedirect(reverse("manage_classes"))
        
        elif "create-student" in dict(request.POST.items()).keys():
            student_form = StudentForm(request.POST, request.FILES)

            if student_form.is_valid():
                print("\n STUDENT FORM VALID \n")
                student_form.save()
                
                return HttpResponseRedirect(reverse("manage_classes"))
            else:
                print("\n STUEDNT FORM INVALID \n")

    else:
        classes = Class.objects.all().order_by("-class_grade")

        class_form = ClassForm()
        student_form = StudentForm()
        context = {
            "class_form": class_form,
            "student_form": student_form,
            "classes":classes,
        }

        return render(request, "photom/manage_classes.html", context)
    
# CLASS MUST BELONG TO THE USER
def class_settings(request, class_id):

    class_instance = get_object_or_404(Class, pk=class_id)

    if request.method == "POST":
        class_form = ClassForm(request.POST, instance=class_instance)

        if class_form.is_valid():

                # Update database object
                class_form.save()
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