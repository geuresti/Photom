from django.shortcuts import render
from django.shortcuts import render
from photom.models import Student, Photo, SchoolAccount
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from photom.forms import StudentForm, PhotoForm
from django.http import FileResponse

from photomanager import settings
import os

# STUDENT MUST BELONG TO THE USER
def student_settings(request, student_id):

    student_instance = get_object_or_404(Student, pk=student_id)

    # Student information is being updated
    if request.method == "POST":

        student_form = StudentForm(request.POST, request.FILES, instance=student_instance)
        old_photo_id = str(student_instance.student_photo_ID)

        if student_form.is_valid():

            # Delete old photo ID before uploading new one
            if 'student_photo_ID' in request.FILES.keys():
                os.remove(os.path.join(settings.MEDIA_ROOT, old_photo_id))
            
            student_form.save()

            render_form = StudentForm(request.POST, instance=student_instance)

            context = {
                "student_id":student_id,
                "student":student_instance,
                "student_form": render_form
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
        photo_form = PhotoForm(request.POST, request.FILES)

        if photo_form.is_valid():
            # REMOVE HARD CODED FOREIGN KEY AFTER TESTING
            harcoded_school = SchoolAccount.objects.get(pk=1)

            new_photo = Photo()
            new_photo.student = student_instance
            new_photo.school_account = harcoded_school
            new_photo.photo = request.FILES['photo']

            new_photo.save()

            print("\n UPLOADED PHOTO TO STUDENT \n")
            
            blank_form = PhotoForm()

            context = {
                "student_id":student_id,
                "student":student_instance,
                "photo_form": blank_form
            }

            return render(request, "photom/view_student.html", context)
        else:
            print("\n UPLOAD IMAGE FAILED \n")
            return HttpResponseRedirect(reverse("manage_classes"))
    else:
        photo_form = PhotoForm()

        context = {
            "student_id":student_id,
            "student":student_instance,
            "photo_form": photo_form
        }

        return render(request, "photom/view_student.html", context)
    
def download_photo(request, photo_id):
    photo = Photo.objects.get(pk=photo_id)
    student_pictures = photo.student.photo_set.all()
    index = 1
    for picture in student_pictures:
        if picture == photo:
            break
        else:
            index += 1

    filename = photo.student.first_name + "_" + photo.student.last_name + "_" + str(index) + ".png"
    return FileResponse(photo.photo, as_attachment=True, filename=filename)

# CLASS MUST BELONG TO THE USER
def delete_student(request, student_id):

    student_instance = get_object_or_404(Student, pk=student_id)
    print("\n STUDENT SUCCESSFULLY DELETED (not actually)\n")
    student_instance.delete()

    return HttpResponseRedirect(reverse("manage_classes"))