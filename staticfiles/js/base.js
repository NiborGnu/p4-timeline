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

// Function to toggle comments section
function toggleComments(id) {
    var commentsSection = document.getElementById('comments-section-' + id);
    var toggleButton = document.getElementById('comment-toggle-' + id);

    if (commentsSection.style.display === 'none' || commentsSection.style.display === '') {
        commentsSection.style.display = 'block'; // Show comments section
        toggleButton.innerHTML = '<i class="fa-solid fa-comments"></i> Hide Comments'; // Change to "Hide Comments"
    } else {
        commentsSection.style.display = 'none'; // Hide comments section
        // Update the button back to show comment count if there are comments
        var commentCount = toggleButton.getAttribute('data-comment-count');
        toggleButton.innerHTML = '<i class="fa-solid fa-comments"></i> <small>' + commentCount + '</small>';
    }
}

// Function to validate the form and enable/disable the save button
function validateForm(id) {
    var bodyElement = document.getElementById("body-" + id);
    var saveButton = document.getElementById("saveBtn-" + id);
    var errorElement = document.getElementById("body-error-" + id);

    if (bodyElement.value.trim() === "") {
        saveButton.disabled = true;
        errorElement.style.display = "block"; // Show the error message
    } else {
        saveButton.disabled = false;
        errorElement.style.display = "none"; // Hide the error message
    }
}