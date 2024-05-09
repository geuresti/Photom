from django.shortcuts import render
from django.shortcuts import render
from photom.models import Student, Photo, SchoolAccount
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from photom.forms import StudentForm, PhotoForm
from django.http import FileResponse
from .views import belongs_to_authenticated_user
from photomanager import settings
from django.contrib.auth.decorators import login_required
import os

# STUDENT MUST BELONG TO THE USER
@login_required
def student_settings(request, student_id):

    # Redirect if user attempting to view a student that isn't theirs
    if not belongs_to_authenticated_user(request.user, student_id, 'student'):
        return HttpResponseRedirect(reverse("index"))
    
    student_instance = get_object_or_404(Student, pk=student_id)
    school = SchoolAccount.objects.get(user=request.user)

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
                "student_form": render_form,
                "school": school
            }

            return render(request, "photom/view_student.html", context)
    
    else:
        student_form = StudentForm(instance=student_instance)

        context = {
            "student_id":student_id,
            "student":student_instance,
            "student_form": student_form,
            "school": school
        }

        return render(request, "photom/student_settings.html", context)
    
# Remove PhotoForm
@login_required
def view_student(request, student_id):
    student_instance = get_object_or_404(Student, pk=student_id)
    school = SchoolAccount.objects.get(user=request.user)
    
    # Redirect if user attempting to view a student that isn't theirs
    if not belongs_to_authenticated_user(request.user, student_id, 'student'):
        return HttpResponseRedirect(reverse("index"))

    if request.method == "POST":
        photo_form = PhotoForm(request.POST, request.FILES)

        if photo_form.is_valid():
            school = SchoolAccount.objects.get(user=request.user)

            new_photo = Photo()
            new_photo.student = student_instance
            new_photo.school_account = school
            new_photo.photo = request.FILES['photo']

            new_photo.save()

            print("\n UPLOADED PHOTO TO STUDENT \n")
            
            blank_form = PhotoForm()

            context = {
                "student_id":student_id,
                "student":student_instance,
                "photo_form": blank_form,
                "school": school
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
            "photo_form": photo_form,
            "school": school
        }

        return render(request, "photom/view_student.html", context)
    
@login_required
def download_photo(request, photo_id):
    # Redirect if user attempting to download a student's photo 
    # that is not associated with one of their classes
    if not belongs_to_authenticated_user(request.user, photo_id, 'photo-id'):
        return HttpResponseRedirect(reverse("index"))

    photo = Photo.objects.get(pk=photo_id)

    # Add an index to the end of the student photo filename
    student_pictures = photo.student.photo_set.all()
    index = 1
    for picture in student_pictures:
        if picture == photo:
            break
        else:
            index += 1

    filename = photo.student.first_name + "_" + photo.student.last_name + "_" + str(index) + ".png"
    return FileResponse(photo.photo, as_attachment=True, filename=filename)

@login_required
def delete_student(request, student_id):

    # Redirect if user attempting to delete a student from a different school
    if not belongs_to_authenticated_user(request.user, student_id, 'student'):
        return HttpResponseRedirect(reverse("index"))
    
    student_instance = get_object_or_404(Student, pk=student_id)
    student_instance.delete()
    print("\n STUDENT SUCCESSFULLY DELETED \n")

    return HttpResponseRedirect(reverse("manage_classes"))