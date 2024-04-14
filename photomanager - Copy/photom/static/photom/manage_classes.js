let classes = document.getElementsByClassName("class-students");
let class_links = document.getElementsByClassName("class-link"); 
let class_display = document.getElementById("class-display"); 

// The first class will be active by default
var active_class = classes[0];
active_class.style.display = "flex";
class_display.innerHTML = class_links[0].innerHTML;

class_links[0].style.borderBottom = "1px solid black";

for (var i = 0; i < class_links.length; i++) {
    let class_index = i;

	class_links[i].addEventListener("click", function() {
        let my_class = classes[class_index];

        // If the display is none, switch it and change active_class
        if (window.getComputedStyle(my_class, null).getPropertyValue("display") === "none") {
            active_class.style.display = "none";
            my_class.style.display = "flex";
            active_class = my_class;

            for (var j = 0; j < class_links.length; j++) {
                class_links[j].style.borderBottom = "none";
            }

            // The active class link will be underlined
            class_links[class_index].style.borderBottom = "1px solid black";
            class_display.innerHTML = class_links[class_index].innerHTML;

        }
	})
}

