from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from photom.models import SchoolAccount, Class, Student, Photo, Notification
from photom.forms import AccountForm, AccountSettingsForm, NotificationForm
from photomanager import settings
import zipfile, pathlib, io, os

########################## GENERAL ##########################

# Helper function for download_school_photos()
def get_school_photos(pk):
    school = SchoolAccount.objects.get(pk=pk)
    school_classes = school.class_set.all()

    photos = []

    # Iterate over all classes from the specified school
    for cls in school_classes:

        # Get photos for the current class
        class_photos = get_class_photos(cls.pk)

        # If there are more than zero portraits, add subset to photos array
        if len(class_photos) > 0:
            class_photos.append(cls.class_name)
            photos.append(class_photos)
    
    return photos

# Download all portraits of a school into a zip file
def download_school_photos(request, pk):
    school_name = SchoolAccount.objects.get(pk=pk).school_name

    photos = get_school_photos(pk)

    media_directory = pathlib.Path(str(settings.MEDIA_ROOT) + "\\student-pictures\\")
                    
    zip_file_name = school_name + " Photos.zip"
    zip_buffer = io.BytesIO()

    # Open zip file
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        # Go through each class subset of photos
        for subset in photos:
            # Look through media folder and see if the photo from the subset exists
            for file_path in media_directory.iterdir():
                file_name = str(file_path).split('\\')[-1]
                # Add image to zip file and add it to a folder named after the class it belongs to             
                if file_name in subset:
                    zip_file.write(file_path, arcname = school_name + "/" + subset[-1] + "/" + file_path.name)

    # Add file to response and return it
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename = %s' % zip_file_name
    return response

def get_class_photos(pk):
    # Get class by id
    clss = Class.objects.get(pk=pk)

    # Get all students that belong to that class
    class_students = clss.student_set.all()

    # Look at every student in the class and check if they
    # have a photo associated with them. If so, add those
    # photos to the array of photo objects 
    photos = []
    for student in class_students:
        #print("\nstudent:", student, "\n")
        filtered_pictures = Photo.objects.filter(student=student)
        if len(filtered_pictures) > 0:
            for picture in filtered_pictures:
                photos.append(str(picture))

    #print("\n photos:", photos, "\n")
    return photos

def download_class_photos(request, pk):
    clss = Class.objects.get(pk=pk)

    # Get a list of all photos to download
    photos = get_class_photos(pk)

    # Go to media directory
    media_directory = pathlib.Path(str(settings.MEDIA_ROOT) + "\\student-pictures\\")

    # Set up zip file
    zip_file_name = clss.class_name + " Photos.zip"
    zip_buffer = io.BytesIO()

    # Open zip file and read through the contents of the media
    # directory. If the photo is in the 'photos' array then
    # add it to the zip file.
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for file_path in media_directory.iterdir():
            file_name = str(file_path).split('\\')[-1]               
            if file_name in photos:
                zip_file.write(file_path, arcname = clss.class_name + "/" + file_path.name)

    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename = %s' % zip_file_name
    return response

# This function organizes the classes by grade descending
def organize_classes(school):
    filetered_classes = Class.objects.filter(class_school=school).order_by("-class_grade")
    num_grades = [cls for cls in filetered_classes if cls.class_grade.isnumeric()]
    let_grades = [cls for cls in filetered_classes if not cls.class_grade.isnumeric()]
    let_grades.reverse()

    organized_classes = num_grades + let_grades
    return organized_classes

# Home page
@login_required
def index(request):

    if request.user.is_superuser:
        return HttpResponseRedirect(reverse('schools_dashboard'))
    
    school = SchoolAccount.objects.get(user=request.user)
    classes = organize_classes(school)
    notifications = Notification.objects.filter(school=school, hidden=False).order_by('-date_sent')
    
    students_that_have_photos = []

    # Track which students have photos so that they will have a check mark
    # added next to their icon in the index template
    for cls in classes:
        for student in cls.student_set.all():
            student_photo = Photo.objects.filter(student=student)
            if len(student_photo) > 0:
                print("\n student:", student, "has photo")
                students_that_have_photos.append(student)

    # classes are needed for main display
    # school and notifications are needed for most views for the header
    context = {
        "notifications":notifications,
        "classes":classes,
        "school":school,
        "students_that_have_photos": students_that_have_photos
    }

    return render(request, "photom/index.html", context)

# The view for creating notifications on the main site.
@login_required
def notifications(request):

    school = SchoolAccount.objects.get(user=request.user)
    
    context = {
        "school": school,
        "notifications": [],
    }

    # The requesting user must be an admin
    if request.user.is_superuser is False:
        return HttpResponseRedirect(reverse("index"))
    
    if request.method == "POST":

        submitted_notification_form = NotificationForm(request.POST)

        if submitted_notification_form.is_valid():
            print("\n NOTIFICATION SUCCESSFULLY CREATED \n")
            submitted_notification_form.save()
            context["success"] = "Notification successfully created"
        else:
            print("\n NOTIFICATION FORM INVALID \n")
            context["errs"] = "Please select a school"

        notification_form = NotificationForm()

        # Manually set the choices of the notifications.school select
        all_schools = SchoolAccount.objects.all()
        school_options = [(-1, 'Select a School')] + [(school.pk, school.school_name) for school in all_schools if school.user.is_active and school.user.is_superuser == False]   

        notification_form.fields['school'].choices = school_options

        context["form"] = notification_form
        return render(request, "photom/notifications.html", context)

    # This branch doesn't do anything unique but the page was not working without it
    else:
        notification_form = NotificationForm()

        all_schools = SchoolAccount.objects.all()
        school_options = [(-1, 'Select a School')] + [(school.pk, school.school_name) for school in all_schools if school.user.is_active and school.user.is_superuser == False]   

        notification_form.fields['school'].choices = school_options

        context["form"] = notification_form
        return render(request, "photom/notifications.html", context)

# This view sets the specified notifcation to be hidden
@login_required
def hide_notification(request, notif_id):

    notif = get_object_or_404(Notification, pk=notif_id)

    # Check that the notification belongs to the authenticated user
    if not belongs_to_authenticated_user(request.user, notif.pk, 'notification'):
        return HttpResponseRedirect(reverse("index"))
    
    notif.hidden = True
    notif.read = True
    notif.save()
    #print("\n HIDING NOTIFICATION #", notif_id, "\n")
    return HttpResponse(notif)

# This view sets the specified notifcation to be hidden
@login_required
def read_notification(request, notif_id):

    notif = get_object_or_404(Notification, pk=notif_id)

    # Check that the notification belongs to the authenticated user
    if not belongs_to_authenticated_user(request.user, notif.pk, 'notification'):
        return HttpResponseRedirect(reverse("index"))
    
    notif.read = True
    notif.save()
    #print("\n NOTIFICATION #", notif_id, "MARKED AS READ \n")
    return HttpResponse(notif)

# This view is for testing. It resets the 'hidden' and 'read' flags on all notifications
def reset_notifications(request):
    notifs = Notification.objects.all()
    for notif in notifs:
        notif.hidden = False
        notif.read = False
        notif.save()
    return HttpResponseRedirect(reverse("index"))

@login_required
def about(request):
    school = SchoolAccount.objects.get(user=request.user)
    notifications = Notification.objects.filter(school=school, hidden=False)
    context = {
        "school": school,
        "notifications": notifications
    }
    return render(request, "photom/about.html", context)

@login_required
def contact(request):
    school = SchoolAccount.objects.get(user=request.user)
    notifications = Notification.objects.filter(school=school, hidden=False)
    context = {
        'school': school,
        "notifications": notifications
    }
    return render(request, "photom/contact.html", context)

@login_required
def schools_dashboard(request):
    school = SchoolAccount.objects.get(user=request.user)
    notifications = Notification.objects.filter(school=school, hidden=False)
    all_schools = SchoolAccount.objects.all()

    filtered_schools = [s for s in all_schools if s.user.is_superuser == False and s.user.is_active == True]

    context = {
        "school": school,
        "notifications": notifications,
        "all_schools": filtered_schools,
    }

    return render(request, "photom/schools_dashboard.html", context)

@login_required
def download_school_csv(request, pk):
    school = SchoolAccount.objects.get(pk=pk)

    # Check that there is a csv to download
    if school.has_csv:
        file_name = school.school_name + ".csv"
        directory = 'student_data\\' + school.school_name + "\\" + file_name
        file_path = os.path.join(settings.BASE_DIR, directory)

        # Check that the file path exists and return file in response
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'
            return response
    
    print("\nERROR: Download failed. Either the school did not have a csv file available or the path was incorrect.\n")
    return HttpResponseRedirect(reverse("index"))
    
# An untested function for deleting school csv files
@login_required
def delete_school_csv(request, pk):
    school = SchoolAccount.objects.get(pk=pk)

    if school.has_csv:
        file_name = school.school_name + ".csv"
        directory = 'student_data\\' + school.school_name + "\\" + file_name
        file_path = os.path.join(settings.BASE_DIR, directory)
        if os.path.exists(file_path):
            os.remove(file_path)

# The view for the search bar results page
@login_required
def search_students(request):

    school = SchoolAccount.objects.get(user=request.user)
    notifications = Notification.objects.filter(school=school, hidden=False)
    context = {
        "school": school,
        "notifications": notifications
    }

    if request.method == "POST":
        searched = request.POST['searched']
        context['searched'] = searched
        search_results = []
        classes = school.class_set.all()

        # If the search is by ID
        if searched.isnumeric():
            # Filter students from the user's school by the searched number
            for cls in classes:
                students_by_id = cls.student_set.filter(student_ID__contains=searched)
                # Add matching students to search results
                for student in students_by_id:
                    search_results.append(student)
            context['search_results'] = search_results
            return render(request, "photom/search_students.html", context)
        # The search is by first or last name
        else:
            searched = searched.capitalize()

            # Filter each student of each class by the searched word
            for cls in classes:
                students_by_name = cls.student_set.filter(first_name__contains=searched) | cls.student_set.filter(last_name__contains=searched)
                # Add matching students to search results
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
# belongs to the authenticated user (or if the user is an admin)
def belongs_to_authenticated_user(user, pk, association):

    if user.is_superuser:
        print("\n ACCESSED BY SUPERUSER \n")
        return True

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

# Create an account using the AccountForm
def create_account(request):
    if request.method == "POST":
        account_form = AccountForm(request.POST)
        if account_form.is_valid():
            print("\n USER SUCCESSFULLY CREATED \n")
            account_form.save()
            return HttpResponseRedirect(reverse("login"))
        else:
            print("\n USER FORM INVALID \n")
            context = {"account_form":account_form}
            return render(request, "registration/create_account.html", context)
    else:
        account_form = AccountForm()
        context = {"account_form":account_form}
        return render(request, "registration/create_account.html", context)
    
@login_required
def account_settings(request):
    
    school = SchoolAccount.objects.get(user=request.user)
    notifications = Notification.objects.filter(school=school, hidden=False)

    if request.method == "POST":
        account_form = AccountSettingsForm(request.POST)
        if account_form.is_valid():
            # Update database object
            print("\n ACCOUNT FORM VALID \n")
            account_form.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            print("\n ACCOUNT FORM INVALID \n")

    # Manually fill out form (due to pk) to display
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
        "school": school,
        "notifications": notifications
    }

    return render(request, "photom/account_settings.html", context)

@login_required
def delete_account(request):
    school_account = get_object_or_404(SchoolAccount, user=request.user)
    # Deactivate account instead of deleting in case of accidental deletion
    school_account.user.is_active = False
    school_account.user.save()
    
    print("\n ACCOUNT SUCCESSFULLY DEACTIVATED \n")
    return HttpResponseRedirect(reverse("login"))

@login_required
def delete_student(request, student_id):

    # Redirect if user attempting to delete a student from a different school
    if not belongs_to_authenticated_user(request.user, student_id, 'student'):
        return HttpResponseRedirect(reverse("index"))
    
    student_instance = get_object_or_404(Student, pk=student_id)
    student_instance.delete()
    print("\n STUDENT SUCCESSFULLY DELETED \n")
    return HttpResponseRedirect(reverse('index'))