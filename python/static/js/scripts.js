// scripts.js

// Confirm deletion of ToDo item
document.addEventListener('DOMContentLoaded', function () {
    const deleteLinks = document.querySelectorAll('.delete-todo');

    deleteLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            if (!confirm('Are you sure you want to delete this ToDo?')) {
                event.preventDefault();
            }
        });
    });
});
