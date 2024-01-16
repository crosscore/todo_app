// static/js/scripts.js
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.status-checkbox').forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            const todoId = this.dataset.id;
            const newStatus = this.checked ? 'completed' : 'pending';
            fetch(`/update/${todoId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `status=${newStatus}`
            }).then(response => {
                if (response.ok) {
                    console.log('Status updated to ${newStatus}');
                } else {
                    console.error('Error updating status');
                }
            });
        });
    });
});

// scripts.js
function moveItem(element, direction) {
    var id = element.getAttribute('data-id');
    fetch(`/move/${id}/${direction}`, {
        method: 'POST'
    }).then(response => {
        if (response.ok) {
            location.reload(); // ページを再読み込みしてリストの順序を更新
        } else {
            console.error('Error moving item');
        }
    });
}
