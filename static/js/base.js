// Function to toggle between post view and edit form
function toggleEdit(id) {
    var viewElement = document.getElementById("timepost-view-" + id);
    var editElement = document.getElementById("edit-form-" + id);

    if (viewElement.style.display === "none") {
        viewElement.style.display = "block"; // Show the TimePost view
        editElement.style.display = "none"; // Hide the edit form
    } else {
        viewElement.style.display = "none"; // Hide the TimePost view
        editElement.style.display = "block"; // Show the edit form
    }
}