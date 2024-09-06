let classes = document.getElementsByClassName("class-students");
let buttons = document.getElementsByClassName("class-button");

if (classes.length !== 0) {

    let class_links = document.getElementsByClassName("class-link"); 
    let class_display = document.getElementById("class-display"); 

    var active_class; 
    var active_class_index;
    let selected_class;

    // Check if there was a previously selected class in local storage
    switch(localStorage.getItem("selected-class")) {
        case null:
            selected_class = 0;
            console.log("no pre selected class");
            break;
        default:
            selected_class = localStorage.getItem("selected-class");
            console.log("pre selected class: ", selected_class);
    }

    // Set the active class to the selected-class from local storage
    // or select the first class by default if there was no selected-class
    active_class = classes[selected_class];
    active_class_index = selected_class;
    class_display.innerHTML = class_links[selected_class].innerHTML;
    class_links[selected_class].style.borderBottom = "1px solid black";
    //class_links[selected_class].style.background = "rgb(255, 255, 255)";

    active_class.style.display = "flex";

    // Set the active button to the selected-class index
    buttons[selected_class].style.display = "inline";

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
            localStorage.setItem("selected-class", class_index);

            // If the display is none, switch it and change active_class
            if (window.getComputedStyle(selected_class, null).getPropertyValue("display") === "none") {
                
                // Change active class display to none and 
                // change the display of the clicked class to flex
                active_class.style.display = "none";
                selected_class.style.display = "flex";

                // Change active download button display to none
                buttons[active_class_index].style.display = "none";

                active_class = selected_class;
                active_class_index = class_index;

                // Remove underline for other class links
                for (var j = 0; j < class_links.length; j++) {
                    class_links[j].style.borderBottom = "none";
                    //class_links[selected_class].style.background = "none";
                }

                // Add underline for active class link
                class_links[class_index].style.borderBottom = "1px solid black";
              //  class_links[selected_class].style.background = "rgb(255, 255, 255)";
                class_display.innerHTML = class_links[class_index].innerHTML;
                
                // Display new download button
                buttons[active_class_index].style.display = "inline";

                // Reset the order option dropdown
                sort_by.value = "order-added";

                // Set the students to be in the order they were added
                let classes_as_array = Array.from(classes[active_class_index].children);
                console.log("\nby order added (active class change)");
                localStorage.setItem("order-style", "order-added")
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
        let last_name_b = b.children[1].innerHTML.split(" ")[1];
        return last_name_a.localeCompare(last_name_b);
    }

    // Sort HTML elements of array by last name
    var sort_by_first_name = function(a, b) {
        let first_name_a = a.children[1].innerHTML.split(" ")[0];
        let first_name_b = b.children[1].innerHTML.split(" ")[0];
        return first_name_a.localeCompare(first_name_b);
    }

    // Sort HTML elements of array by order added (primary key order)
    var sort_by_order_added = function(a, b) {
        let primary_key_a = a.children[0].children[0].innerHTML;
        let primary_key_b = b.children[0].children[0].innerHTML;
        return primary_key_a - primary_key_b;
    }

    // Sort HTML elements of array by most recent (primary key order reversed)
    var sort_by_most_recent = function(a, b) {
        let primary_key_a = a.children[0].children[0].innerHTML;
        let primary_key_b = b.children[0].children[0].innerHTML;
        return primary_key_b - primary_key_a;
    }

    var sort_by_has_portrait = function(a, b) {
        let element_a = a.children[0].children[2];
        let element_b = b.children[0].children[2];

        a_has_portrait = element_a.classList.contains("has-portrait");
        b_has_portrait = element_b.classList.contains("has-portrait");

        return (a_has_portrait && b_has_portrait == false) ? -1 : 1;
    }

    // On document load, set the order of the students to "Order Added"
    document.addEventListener("DOMContentLoaded", (event) => {
        let classes_as_array = Array.from(classes[active_class_index].children);

        // Get the most recently selected order style from local storage
        let order_style = localStorage.getItem("order-style");
        let class_by_order_style;

        let dropdown = document.getElementById("sort-by");
        
        // Set the class_by_order_style based on the order_style
        switch(order_style) {
            case "most-recent":
                class_by_order_style = classes_as_array.toSorted(sort_by_most_recent);
                dropdown.selectedIndex = 1;
                break;
            case "last-name":
                class_by_order_style = classes_as_array.toSorted(sort_by_last_name);
                dropdown.selectedIndex = 2;
                break;
            case "first-name":
                class_by_order_style = classes_as_array.toSorted(sort_by_first_name);
                dropdown.selectedIndex = 3;
                break;
            case "has-portrait":
                class_by_order_style = classes_as_array.toSorted(sort_by_has_portrait);
                dropdown.selectedIndex = 4;
                break;
            default:
                dropdown.selectedIndex = 0;
                class_by_order_style = classes_as_array.toSorted(sort_by_order_added);
        }

        console.log("order style: ", order_style)

        // Organize the students being displayed
        sort_students(active_class_index, class_by_order_style);
    });

    // When the Sort Students dropdown is updated, set the order to the selected value
    sort_by.onchange = function() {

        let classes_as_array = Array.from(classes[active_class_index].children);

        // Sort students based on the four order options
        switch(sort_by.value) {
            case "order-added":
                let class_by_order_added = classes_as_array.toSorted(sort_by_order_added);
                console.log("\nby order added");
                localStorage.setItem("order-style", "order-added")
                sort_students(active_class_index, class_by_order_added);
                break;
            case "most-recent":
                let class_by_most_recent = classes_as_array.toSorted(sort_by_most_recent);
                console.log("\nby most recent");
                localStorage.setItem("order-style", "most-recent")
                sort_students(active_class_index, class_by_most_recent);
                break;
            case "last-name":
                console.log("\nby last name");
                let class_by_last_name = classes_as_array.toSorted(sort_by_last_name);
                localStorage.setItem("order-style", "last-name")
                sort_students(active_class_index, class_by_last_name);
                break;
            case "first-name":
                console.log("\nby first name");
                let class_by_first_name = classes_as_array.toSorted(sort_by_first_name);
                localStorage.setItem("order-style", "first-name")
                sort_students(active_class_index, class_by_first_name);
                break;
            case "has-portrait":
                console.log("\nby has portrait");
                let class_by_has_portrait = classes_as_array.toSorted(sort_by_has_portrait);
                localStorage.setItem("order-style", "has-portrait")
                sort_students(active_class_index, class_by_has_portrait);
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
            new_element.classList.add("index-student-card");

            // Update HTML with each new student card
            class_to_update.appendChild(new_element);
        }
        
        //display_students(sorted_class);
    }
}
