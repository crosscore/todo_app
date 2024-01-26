// static/js/scripts.js

// 変数定義
const API_CALL_WAIT_TIME = 180000;

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

function updateDate() {
    var now = new Date();
    var dateString = now.getFullYear() + '-' + (now.getMonth() + 1) + '-' + now.getDate() + ' ' + now.getHours() + ':' + now.getMinutes() + ':' + now.getSeconds();
    $('#current-date').text(dateString);
}

$(document).ready(function(){
    // 天気情報を取得する関数
    function getWeather() {
        var lastCall = localStorage.getItem('lastWeatherCall');
        var now = new Date().getTime();

        // キャッシュされたデータを使用する条件をチェック
        if (lastCall && now - lastCall < API_CALL_WAIT_TIME) {
            var cachedData = JSON.parse(localStorage.getItem('weatherData'));
            if (cachedData) {
                updateWeatherInfo(cachedData);
                return;
            }
        }

        // APIからデータを取得
        $.getJSON('/weather', function(data) {
            // 新しい天気情報を表示
            updateWeatherInfo(data);

            // 新しい天気情報をローカルストレージに保存
            localStorage.setItem('weatherData', JSON.stringify(data));
            localStorage.setItem('lastWeatherCall', now);
        });
    }

    // 天気情報を表示する関数
    function updateWeatherInfo(data) {
        $('#temperature').text(data.temperature + '°C');
        $('#weather').text(data.weather + ' in ' + data.location);
        $('#location').text(data.location);
    }

    // 初回のページ読み込み時に天気情報を取得
    getWeather();

    // 初回の呼び出しからAPI_CALL_WAIT_TIME秒後に定期的な更新を開始
    setInterval(getWeather, API_CALL_WAIT_TIME);
});
