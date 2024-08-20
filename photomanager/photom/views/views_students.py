from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, FileResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from django.contrib import messages
from photom.models import Student, Class, Photo, SchoolAccount, Notification
from photom.forms import StudentForm, PhotoForm, CSVUploadForm, ImagesForm
from .views import belongs_to_authenticated_user
from photomanager import settings
import os, csv

# Class based view to handle a multi-image file upload
class FileFieldFormView(FormView):
    form_class = ImagesForm
    template_name = "photom/upload_photos.html"
    success_url = "success"

    # Adjust the context
    def get_context_data(self, *args, **kwargs):
        context = super(FileFieldFormView, self).get_context_data(*args,**kwargs)
        users = User.objects.filter(is_superuser=True)
        if len(users) > 0:
            admin = users[0]
            school = SchoolAccount.objects.get(user=admin)
            context['school'] = school
        return context

    def form_valid(self, form):
        school_id = form.cleaned_data['school']
        # This implies the user left the school option blank
        if school_id == '-1':
            print("\n ERROR: please select a school \n")
            messages.add_message(self.request, messages.ERROR, "Please select a school.")
            return HttpResponseRedirect(self.request.path_info)
        # Set the 'school' to the selected value
        else:
            school = SchoolAccount.objects.get(pk=school_id)
            files = form.cleaned_data["photos"]
            print("\n SCHOOL SELECTED: ", school)

        classes = school.class_set.all()

        # Create a list of all students from all classes of 
        # the given school in order to check their ID numbers
        filtered_students = []
        for cls in classes:
            students = cls.student_set.all()
            for s in students:
                filtered_students.append(s)
        
        # Iterate over photos
        for f in files:

            # Extract id from filename
            if "_" in f.name:
                delim = '_'
            else:
                delim = '.'

            photo_student_id = f.name[:f.name.index(delim)]

            #print("\nFILE NAME:", photo_student_id, "\n")

            # Check that it's numeric
            if photo_student_id.isnumeric():
                # Iterate over students and match the id    
                for student in filtered_students:
                    # Create a new photo
                    if student.student_ID == int(photo_student_id):
                        # Check if student already has a photo with that ID
                        photos = student.photo_set.all()

                        for p in photos:
                            p_name = str(p)

                            if "_" in p_name:
                                delimiter = '_'
                            else:
                                delimiter = '.'

                            photo_id = p_name[:p_name.index(delimiter)]

                            if photo_id == photo_student_id:
                                print("\n removing old photo:", str(p))
                                os.remove(os.path.join(settings.MEDIA_ROOT, "student-pictures\\" + str(p)))
                                p.delete()

                        photo = Photo(
                          photo=f,
                          student=student
                        )

                        photo.save()
                        print("\n PHOTO SAVED TO STUDENT (enabled)")
                        break
                else:
                    print("\nERROR: STUDENT ID", photo_student_id, "NOT FOUND")  
            else:
                print("\nERROR: WRONG FILE NAME\n")
        return super().form_valid(form)

# This is a workaround for the FormView only allowing a 'success_url'
# This is used when the user successfully uploads images from the FormView   
def reset_image_upload(request):
    messages.add_message(request, messages.SUCCESS, "Image(s) successfully uploaded.")
    return HttpResponseRedirect(reverse("upload_photos"))
    
@login_required
def upload_csv(request):

    errs = None
    school = SchoolAccount.objects.get(user=request.user)
    notifications = Notification.objects.filter(school=school, hidden=False)

    csv_form = CSVUploadForm()
    all_schools = SchoolAccount.objects.all()

    # Set csv form dropdown options
    school_options = [(-1, 'Select a School')] + [(school.pk, school.school_name) for school in all_schools if school.user.is_active and school.user.is_superuser == False]   
    csv_form.fields['school'].choices = school_options

    context = {
        "school": school,
        "csv_form": csv_form,
        "notifications": notifications
    }

    if request.method == "POST":
        # Check that there is an csv file in the request
        if request.FILES["csv_file"]:
            school_id = request.POST.get('school')
            # Check if the user is an admin
            if request.user.is_superuser:
                # Check that the admin selected a school to upload the file to
                if school_id == '-1':
                    print("\n ERROR: please select a school \n")
                    errs = ('You must select a school')
                    context["errs"] = errs
                    return render(request, "photom/upload_csv.html", context)
                # Update the school's classes and students
                else:
                    school_to_update = SchoolAccount.objects.get(pk=school_id)
            else:
                school_to_update = school

            # If the user is not an admin, update the user's school
            print("\nSchool to update:", school_to_update, "\n")
            f = request.FILES["csv_file"]
            file_name = "/" + school_to_update.school_name + ".csv"

            # Check if the school's file exists
            # If not, make a new directory using the school's name
            if os.path.exists("student_data/" + school_to_update.school_name) == False:
                print("\nDirectory doesn't exist\n")
                os.mkdir("student_data/" + school_to_update.school_name)
            else:
                print("\nDirectory DOES exist\n")

            file_path = "student_data/" + school_to_update.school_name + file_name

            # Add .csv file to the student data folder
            with open(file_path, "wb+") as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

            # Update the school's classes and students
            return read_students_csv(request, file_path, school_to_update)
        else:
            print("\nERROR: Received non csv file\n")

    return render(request, "photom/upload_csv.html", context)

@login_required
def read_students_csv(request, file_path, school):
    csv_form = CSVUploadForm()
    errors = []
    new_classes = []
    csv_file_content = []

    # Open the file path provided and add the content to 'csv_file_content'
    with open(file_path, mode ='r') as f:    
        csvFile = csv.DictReader(f)
        for lines in csvFile:
            csv_file_content.append(lines)
    
    correct_keys = ['Student Last Name', 'Student First Name', 'Grade', 'Teacher', 'Id Number']

    # Check each row to make sure the file is in the correct format
    for row in csv_file_content:
        for key in correct_keys:
            if key not in row.keys():
                print("\n ERROR: Incorrectly formatted csv file \n")
                context = {
                    "csv_form": csv_form,
                    "errs": "Incorrectly formatted file was given"
                }
                return render(request, "photom/upload_csv.html", context)
    
    school_classes = school.class_set.all()

    # Create classes from csv file
    for row in csv_file_content:
        print("read row content...")

        class_already_exists = False
       # print("\n", row, "\n")
        student_class = Class.objects.filter(class_teacher=row['Teacher'])

        # Check if the class already exists in the query results
        for sc in student_class:
            # Check if queried class exists for this school specifically
            if sc in school_classes:
                class_already_exists = True
                break

        # Create new class
        if not class_already_exists and row['Teacher'] not in new_classes:
            new_class = Class(
                class_name = row['Teacher'].strip() + " " + row['Grade'].strip(),
                class_teacher = row['Teacher'].strip(),
                class_grade = row['Grade'].strip(),
                class_school = school
            )

            new_classes.append(new_class.class_teacher)
            new_class.save()
            print("\n MADE NEW CLASS (enabled) \n")
        else:
            print("\n class arleady exists, skipping \n")

    # Add students to classes in csv file
    for row in csv_file_content:

        class_to_add_student_to = school.class_set.filter(class_teacher=row['Teacher'])[0]
    
        # Check if the class grade and student grade correspond
        if class_to_add_student_to.class_grade == row['Grade']:

            student_check = class_to_add_student_to.student_set.all()
            student_ids = [stdnt.student_ID for stdnt in student_check]

            # Check if the student (by id) already exists in this class
            if int(row['Id Number']) not in student_ids:

                # Create a new student
                print("\n student isnt in my class yet yipeee")
                student = Student(
                    first_name = row['Student First Name'].strip(),
                    last_name = row['Student Last Name'].strip(),
                    student_class = class_to_add_student_to,
                    student_ID = row['Id Number'].strip()
                )            

                student.save()
                print("\n STUDENT ADDED (enabled)\n")
          #  else:
                #err_str = "Student already in class:", row['Student First Name'], row['Student Last Name']
               # errors.append(err_str)
                #continue
        else:
            err_str = "Student grade and class grade did not match for: not found for student:", row['Student First Name'], row['Student Last Name']
            errors.append(err_str)
            continue

    # Print errors to console
    for error in errors:
        print("\nERR:", error)

    school.has_csv = True
    school.save()
    
    context = {
        "school": school,
        "csv_form": csv_form,
        "success": "Successfully uploaded csv"
    }

    return render(request, "photom/upload_csv.html", context)

@login_required
def student_settings(request, student_id):

    # Redirect if user attempting to view a student that isn't theirs
    if not belongs_to_authenticated_user(request.user, student_id, 'student'):
        return HttpResponseRedirect(reverse("index"))
    
    student_instance = get_object_or_404(Student, pk=student_id)
    school = SchoolAccount.objects.get(user=request.user)
    notifications = Notification.objects.filter(school=school, hidden=False)

    # Student information is being updated
    if request.method == "POST":

        student_form = StudentForm(request.POST, request.FILES, instance=student_instance, user=request.user)
        #old_photo_id = str(student_instance.student_photo_ID)

        if student_form.is_valid():

            # Delete old photo ID before uploading new one
          #  if 'student_photo_ID' in request.FILES.keys():
          #      os.remove(os.path.join(settings.MEDIA_ROOT, old_photo_id))
            
            student_form.save()

            render_form = StudentForm(request.POST, instance=student_instance, user=request.user)

            context = {
                "student_id":student_id,
                "student":student_instance,
                "student_form": render_form,
                "school": school,
                "notifications": notifications
            }

            #return render(request, "photom/index.html", context)
            return HttpResponseRedirect(reverse('index'))
    else:
        # Display form and update context
        student_form = StudentForm(instance=student_instance, user=request.user)
        context = {
            "student_id":student_id,
            "student":student_instance,
            "student_form": student_form,
            "school": school,
            "notifications": notifications
        }
        return render(request, "photom/student_settings.html", context)
    
# Note: This view is currently unused
@login_required
def view_student(request, student_id):
    # Note: PhotomForm likely no longer needed

    student_instance = get_object_or_404(Student, pk=student_id)
    school = SchoolAccount.objects.get(user=request.user)
    notifications = Notification.objects.filter(school=school, hidden=False)

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
                "school": school,
                "notifications": notifications
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
            "school": school,
            "notifications": notifications
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

    # Set filename and return response containing the file
    filename = photo.student.first_name + "_" + photo.student.last_name + "_" + str(index) + ".png"
    return FileResponse(photo.photo, as_attachment=True, filename=filename)

@login_required
def delete_student(request, student_id):

    # Redirect if user attempting to delete a student from a different school
    if not belongs_to_authenticated_user(request.user, student_id, 'student'):
        return HttpResponseRedirect(reverse("index"))
    
    student_instance = get_object_or_404(Student, pk=student_id)
    student_instance.delete()
    print("\n STUDENT SUCCESSFULLY DELETED (ENABLED) \n")
    return HttpResponseRedirect(reverse("manage_classes"))