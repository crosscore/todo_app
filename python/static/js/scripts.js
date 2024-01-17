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

function moveItem(element, direction) {
    var id = element.getAttribute('data-id');
    var li = element.closest('li');
    var nextLi = direction === 'up' ? li.previousElementSibling : li.nextElementSibling;

    if (nextLi) {
        li.classList.add(direction === 'up' ? 'slide-fade-up' : 'slide-fade-down');
        nextLi.classList.add(direction === 'up' ? 'slide-fade-down' : 'slide-fade-up');

        setTimeout(function() {
            // アニメーション後にDOMの更新を行う
            if (direction === 'up') {
                li.parentNode.insertBefore(li, nextLi);
            } else {
                li.parentNode.insertBefore(nextLi, li);
            }

            // アニメーションクラスの削除
            li.classList.remove('slide-fade-up', 'slide-fade-down');
            nextLi.classList.remove('slide-fade-up', 'slide-fade-down');

            // 完全なアニメーションの完了を待つ
            setTimeout(function() {
                location.reload();
            }, 300);
        }, 250); // アニメーション時間
    }

    fetch(`/move/${id}/${direction}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    }).then(response => {
        if (!response.ok) {
            console.error('Error moving item');
        }
    });
}
