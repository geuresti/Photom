from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from photom.models import Student, Class
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from photom.forms import ClassForm, StudentForm, UploadFileForm

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
            print("\n form data: ", student_form.data, "\n")
            print("\n received photo id: ", request.FILES)
           # print("\n form data asd: ", type(student_form.data["student_photo_ID"]), "\n")

            if student_form.is_valid():
                print("STUEDNT FORM VALID \n")

               # print("\n files data: ", request.FILES['student_photo_ID'], "\n")
                #image_file = request.FILES['student_photo_ID'].file.read()
              #  print("\n image file:", image_file, "\n")

                new_student = Student()

                assigned_class = get_object_or_404(Class, pk=student_form.data["student_class"])
                #print("\n assigned class: ", assigned_class, "\n")

                new_student.first_name=student_form.data["first_name"]
                new_student.last_name=student_form.data["last_name"]
                new_student.student_age=student_form.data["student_age"]
                new_student.student_class=assigned_class
                new_student.student_ID=student_form.data["student_ID"]

                new_student.save()
                
                return HttpResponseRedirect(reverse("manage_classes"))
            else:
                print("STUEDNT FORM NOOOTTTT VALID \n")

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