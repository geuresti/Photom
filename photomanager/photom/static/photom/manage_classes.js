let classes = document.getElementsByClassName("class-students");

//localStorage.clear();

if (classes.length !== 0) {
    let class_links = document.getElementsByClassName("class-link"); 
    let class_display = document.getElementById("class-display"); 
    
    var active_class; 
    var active_class_index;
    let selected_class;

    // Check if there was a previously selected class in local storage
    switch(localStorage.getItem("mc-selected-class")) {
        case null:
            selected_class = 0;
            console.log("no pre selected class");
            break;
        default:
            selected_class = localStorage.getItem("mc-selected-class");
            console.log("pre selected class: ", selected_class);
    }

    // Set the active class to the mc-selected-class from local storage
    // or select the first class by default if there was no mc-selected-class
    active_class = classes[selected_class];
    active_class_index = selected_class;
    class_display.innerHTML = class_links[selected_class].innerHTML;
    class_links[selected_class].style.borderBottom = "1px solid black";

    active_class.style.display = "flex";
    
    for (var i = 0; i < class_links.length; i++) {
        let class_index = i;
    
        class_links[i].addEventListener("click", function() {
            let my_class = classes[class_index];
            localStorage.setItem("mc-selected-class", class_index);

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
}