// Function to toggle between post view and edit form
function toggleEdit(id) {
    var viewElement = document.getElementById("timepost-view-" + id);
    var editElement = document.getElementById("edit-form-" + id);
    var bodyElement = document.getElementById("body-" + id);

    // If the edit form is being shown, store the current value of the text area
    if (viewElement.style.display === "none") {
        // Show the TimePost view
        viewElement.style.display = "block";
        // Hide the edit form
        editElement.style.display = "none";
    } else {
        // Store the original value as a data attribute
        bodyElement.setAttribute('data-original-value', bodyElement.value);

        // Hide the TimePost view
        viewElement.style.display = "none";
        // Show the edit form
        editElement.style.display = "block";
    }
}

// Function to revert the changes made in the edit form
function cancelEdit(id) {
    var bodyElement = document.getElementById("body-" + id);

    // Restore the original value from the stored data attribute
    var originalValue = bodyElement.getAttribute('data-original-value');
    if (originalValue !== null) {
        bodyElement.value = originalValue;
    }

    // Hide the edit form and show the view mode
    toggleEdit(id);
}

// Function to toggle comments section
function toggleComments(id) {
    var commentsSection = document.getElementById('comments-section-' + id);
    var toggleButton = document.getElementById('comment-toggle-' + id);

    if (commentsSection.style.display === 'none' || commentsSection.style.display === '') {
        // Show comments section
        commentsSection.style.display = 'block';
        // Change to "Hide Comments"
        toggleButton.innerHTML = '<i class="fa-solid fa-comments"></i> Hide Comments';
    } else {
        // Hide comments section
        commentsSection.style.display = 'none';
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
        // Show the error message
        errorElement.style.display = "block";
    } else {
        saveButton.disabled = false;
        // Hide the error message
        errorElement.style.display = "none";
    }
}

// Function to revert changes in the edit comment modal
function cancelCommentEdit(id) {
    var commentBodyElement = document.querySelector("#editCommentModal-" + id + " textarea[name='comment_body']");
    var originalValue = commentBodyElement.getAttribute('data-original-value');

    if (originalValue !== null) {
        commentBodyElement.value = originalValue;
    }

    // Hide the modal
    var modal = document.getElementById("editCommentModal-" + id);
    var modalInstance = bootstrap.Modal.getInstance(modal);
    if (modalInstance) {
        modalInstance.hide();
    }
}

// Ensure that the original comment value is set when the modal is opened
document.addEventListener('show.bs.modal', function (event) {
    var button = event.relatedTarget;
    var commentId = button.getAttribute('data-bs-target').split('-')[1];
    var modal = document.getElementById('editCommentModal-' + commentId);
    var textarea = modal.querySelector('textarea[name="comment_body"]');

    // Store the original value
    textarea.setAttribute('data-original-value', textarea.value);
});