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

// Function to confirm deletion of a TimePost
function confirmDelete(event) {
    if (!confirm("Are you sure you want to delete this post?")) {
        event.preventDefault(); // Prevent the form from submitting
        return false;
    }
    return true;
}