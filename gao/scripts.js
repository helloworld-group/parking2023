document.addEventListener("DOMContentLoaded", function () {
    var map = L.map('map').setView([51.505, -0.09], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    var points = [];

    function updateMap() {
        // 清除现有的标记
        map.eachLayer(function (layer) {
            if (layer instanceof L.Marker) {
                map.removeLayer(layer);
            }
        });

        // 添加新标记
        points.forEach(point => {
            L.marker([point.y, point.x]).addTo(map);
        });
    }

    document.getElementById("add-point").addEventListener("click", function () {
        var x = parseFloat(document.getElementById("x-coordinate").value);
        var y = parseFloat(document.getElementById("y-coordinate").value);
        fetch('/add_point', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({x: x, y: y})
        }).then(response => response.json()).then(data => {
            points = data;
            updateMap();
        });
    });

    document.getElementById("delete-point").addEventListener("click", function () {
        var x = parseFloat(document.getElementById("x-coordinate").value);
        var y = parseFloat(document.getElementById("y-coordinate").value);
        fetch('/delete_point', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({x: x, y: y})
        }).then(response => response.json()).then(data => {
            points = data;
            updateMap();
        });
    });

    document.getElementById("execute").addEventListener("click", function () {
        fetch('/execute', {
            method: 'POST'
        }).then(response => response.json()).then(data => {
            alert(data.message);
        });
    });
});