var modals = document.getElementsByClassName("modal");
var student_photos = document.getElementsByClassName("student-photo");
var modal_images = document.getElementsByClassName("modal-image");
var close_buttons = document.getElementsByClassName("close-button");

for (var i = 0; i < student_photos.length; i++) {
    let index = i;

    // Add event listeners to all student photos to trigger the modal
	student_photos[i].addEventListener("click", function() {
        modals[index].style.display = "flex";
        modal_images[index].src = this.src;
	})

    // Add event listeners to all close buttons
    close_buttons[i].addEventListener("click", function() {
        modals[index].style.display = "none";
	})
}