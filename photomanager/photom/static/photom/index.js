let classes = document.getElementsByClassName("class-students");
let class_links = document.getElementsByClassName("class-link"); 
let class_display = document.getElementById("class-display"); 

// The first class will be active by default
var active_class = classes[0];
var active_class_index = 0;
active_class.style.display = "flex";
class_display.innerHTML = class_links[0].innerHTML;

class_links[0].style.borderBottom = "1px solid black";

var sort_by = document.getElementById("sort-by");

/* 
  Add an event listener to each class link in order to:
    - Add an underline to the active class
    - Change the class display to the selected class
    - Reset the value of the 'Sort Students' dropdown
    - Reset the order of the students displayed to be 'Order Added'
*/
for (var i = 0; i < class_links.length; i++) {
    let class_index = i;

	class_links[i].addEventListener("click", function() {
        let selected_class = classes[class_index];

        // If the display is none, switch it and change active_class
        if (window.getComputedStyle(selected_class, null).getPropertyValue("display") === "none") {
            
            // Change active class display to none and 
            // change the display of the clicked class to flex
            active_class.style.display = "none";
            selected_class.style.display = "flex";
            active_class = selected_class;
            active_class_index = class_index;

            // Remove underline for other class links
            for (var j = 0; j < class_links.length; j++) {
                class_links[j].style.borderBottom = "none";
            }

            // Add underline for active class link
            class_links[class_index].style.borderBottom = "1px solid black";
            class_display.innerHTML = class_links[class_index].innerHTML;
            
            // Reset the order option dropdown
            sort_by.value = "order-added";

            // Set the students to be in the order they were added
            let classes_as_array = Array.from(classes[active_class_index].children);
            console.log("\nby order added (active class change)");
            let class_by_order_added = classes_as_array.toSorted(sort_by_order_added);
            sort_students(active_class_index, class_by_order_added);
        }
	})
}

// Display students within the class to console (for testing)
function display_students(html_arr) {
    console.log("\n Sorted Students: \n");
    for (var k = 0; k < html_arr.length; k++) {
        console.log("student: ", html_arr[k].children[1].innerHTML);
    }
}

// Sort HTML elements of array by last name
var sort_by_last_name = function(a, b) {
    let last_name_a = a.children[1].innerHTML.split(" ")[1];
    let last_name_b = b.children[1].innerHTML.split(" ")[1]
    return last_name_a.localeCompare(last_name_b);
}

// Sort HTML elements of array by last name
var sort_by_first_name = function(a, b) {
    let first_name_a = a.children[1].innerHTML.split(" ")[0];
    let first_name_b = b.children[1].innerHTML.split(" ")[0]
    return first_name_a.localeCompare(first_name_b);
}

// Sort HTML elements of array by order added (primary key order)
var sort_by_order_added = function(a, b) {
    let primary_key_a = a.children[0].children[0].innerHTML
    let primary_key_b = b.children[0].children[0].innerHTML
    return primary_key_a - primary_key_b;
}

// Sort HTML elements of array by most recent (primary key order reversed)
var sort_by_most_recent = function(a, b) {
    let primary_key_a = a.children[0].children[0].innerHTML
    let primary_key_b = b.children[0].children[0].innerHTML
    return primary_key_b - primary_key_a;
}

// On document load, set the order of the students to "Order Added"
document.addEventListener("DOMContentLoaded", (event) => {
    let classes_as_array = Array.from(classes[active_class_index].children);
    let class_by_order_added = classes_as_array.toSorted(sort_by_order_added);
    sort_students(active_class_index, class_by_order_added);
});

// When the Sort Students dropdown is updated, set the order to the selected value
sort_by.onchange = function() {

    let classes_as_array = Array.from(classes[active_class_index].children);

    // Sort students based on the four order options
    switch(sort_by.value) {
        case "order-added":
            let class_by_order_added = classes_as_array.toSorted(sort_by_order_added);
            console.log("\nby order added");
            sort_students(active_class_index, class_by_order_added);
            break;
        case "most-recent":
            let class_by_most_recent = classes_as_array.toSorted(sort_by_most_recent);
            console.log("\nby most recent");
            sort_students(active_class_index, class_by_most_recent);
            break;
        case "last-name":
            console.log("\nby last name");
            let class_by_last_name = classes_as_array.toSorted(sort_by_last_name);
            sort_students(active_class_index, class_by_last_name);
            break;
        case "first-name":
            console.log("\nby first name");
            let class_by_first_name = classes_as_array.toSorted(sort_by_first_name);
            sort_students(active_class_index, class_by_first_name);
            break;
        default:
            console.log("Error: Sort By Value Unkown");
    }
}

// 'index' is the class I want to replace
// 'sorted' class is the sorted elements array
function sort_students(index, sorted_class) {
    let class_to_update = document.getElementsByClassName("class-students")[index];
    class_to_update.innerHTML = "";

    // Add the sorted list of students to the HTML document 
    for(let i = 0; i < sorted_class.length; i++) {
        let new_element = document.createElement("div");

        // Add each student from the sorted student list into a <div> tag
        new_element.innerHTML = sorted_class[i].innerHTML;
        new_element.classList.add("student-card");

        // Update HTML with each new student card
        class_to_update.appendChild(new_element);
    }
    
    //display_students(sorted_class);
}