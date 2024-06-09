from django.shortcuts import render
from django.shortcuts import render
from photom.models import Student, Class, Photo, SchoolAccount
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from photom.forms import StudentForm, PhotoForm, CSVUploadForm
from django.http import FileResponse
from .views import belongs_to_authenticated_user
from photomanager import settings
from django.contrib.auth.decorators import login_required
import os
import csv

from csv import DictReader
from io import TextIOWrapper

LAST_NAME = 0
FIRST_NAME = 1
GRADE = 2
TEACHER = 3
ID_NUMBER = 4

def upload_csv(request):

    if request.method == "POST":
        print("\nFILES:", request.FILES, "\n")

        read_students_csv(request, request.FILES["csv_file"])
      #  if form.is_valid():
         #   handle_uploaded_file(request.FILES["file"])
         #   return HttpResponseRedirect("/success/url/")
    else:
        print("\n ERR RRR \n")

    return HttpResponseRedirect(reverse("manage_classes"))

@login_required
def read_students_csv(request, file):
   # print("\n read_students_csv() CALLED \n")

    errors = []

    school = SchoolAccount.objects.get(user=request.user)

    print("\nSCHOOL:", school)

    rows = TextIOWrapper(file, encoding="utf-8", newline="")

    csv_file_content = list(csv.DictReader(rows))

    # Create classes from csv file
    for row in csv_file_content:
        #print("\n", row, "\n")
        student_class = Class.objects.filter(class_teacher=row['Teacher'])

        # Check if the class already exists
        if len(student_class) == 0:

            # Create new class
            new_class = Class(
                class_name = row['Teacher'] + " " + row['Grade'],
                class_teacher = row['Teacher'],
                class_grade = row['Grade'],
                class_school = school
            )

            new_class.save()

    # Add students to classes in csv file
    for row in csv_file_content:
        
        class_set = Class.objects.filter(class_teacher=row['Teacher'])

        # Check if class exists
        if len(class_set) == 0:
            err_str = "Class not found for:", row['Student First Name'], row['Student Last Name']
            errors.append(err_str)
            continue

        student_class = class_set[0]

        # Check if the student and class' grade correspond
        if student_class.class_grade != row['Grade']:
            err_str = "Student grade and class grade did not match for: not found for student:", row['Student First Name'], row['Student Last Name']
            errors.append(err_str)
            continue

        student_check = Student.objects.filter(student_ID = row['Id Number'])

        # Check if the student is already in the class roster
        if len(student_check) > 0:
            continue

        # Create new student
        student = Student(
            first_name = row['Student First Name'],
            last_name = row['Student Last Name'],
            student_class = student_class,
            student_ID = row['Id Number']
        )            

        student.save()

    for error in errors:
        print("\nERR:", error)

    return HttpResponseRedirect(reverse("manage_classes"))

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

        student_form = StudentForm(request.POST, request.FILES, instance=student_instance, user=request.user)
        old_photo_id = str(student_instance.student_photo_ID)

        if student_form.is_valid():

            # Delete old photo ID before uploading new one
            if 'student_photo_ID' in request.FILES.keys():
                os.remove(os.path.join(settings.MEDIA_ROOT, old_photo_id))
            
            student_form.save()

            render_form = StudentForm(request.POST, instance=student_instance, user=request.user)

            context = {
                "student_id":student_id,
                "student":student_instance,
                "student_form": render_form,
                "school": school
            }

            return render(request, "photom/view_student.html", context)
    
    else:
        student_form = StudentForm(instance=student_instance, user=request.user)

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
   # student_instance.delete()
    print("\n STUDENT SUCCESSFULLY DELETED (DISABLED) \n")

    return HttpResponseRedirect(reverse("manage_classes"))