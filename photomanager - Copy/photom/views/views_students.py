from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from photom.models import Student, Class
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from photom.forms import ClassForm, StudentForm, UploadFileForm

# STUDENT MUST BELONG TO THE USER
def student_settings(request, student_id):

    student_instance = get_object_or_404(Student, pk=student_id)

    if request.method == "POST":

        student_form = StudentForm(request.POST, instance=student_instance)
    
        if student_form.is_valid():
            print("\n Student form is valid \n")
            student_form.save()

            context = {
                "student_id":student_id,
                "student":student_instance,
                "student_form": student_form
            }

            return render(request, "photom/view_student.html", context)
    
    else:
        student_form = StudentForm(instance=student_instance)

        context = {
            "student_id":student_id,
            "student":student_instance,
            "student_form": student_form
        }

        return render(request, "photom/student_settings.html", context)
    
# STUDENT MUST BELONG TO THE USER
def view_student(request, student_id):
    student_instance = get_object_or_404(Student, pk=student_id)
    
    if request.method == "POST":
        file_form = UploadFileForm(request.POST, request.FILES)

        print("\n FILE CONTENTS", request.FILES['image'], "\n")

        if file_form.is_valid():

                # Update database object
                student_instance.student_photos.append(request.FILES['image'])
                student_instance.save()
                print("\n UPDATED STUDENT WITH NEW PICTURE \n")
                
                blank_form = UploadFileForm()

                context = {
                    "student_id":student_id,
                    "student":student_instance,
                    "file_form": blank_form
                }

                return render(request, "photom/view_student.html", context)
        else:
                print("\n UPLOAD IMAGE FAILED \n")
                return HttpResponseRedirect(reverse("manage_classes"))
    else:
        file_form = UploadFileForm()

        context = {
            "student_id":student_id,
            "student":student_instance,
            "file_form": file_form
        }

        return render(request, "photom/view_student.html", context)

# CLASS MUST BELONG TO THE USER
def delete_student(request, student_id):

    student_instance = get_object_or_404(Student, pk=student_id)
    print("\n STUDENT SUCCESSFULLY DELETED (not actually)\n")
   # student_instance.delete()

    return HttpResponseRedirect(reverse("manage_classes"))