let map = L.map('map').setView([51.1694, 71.4491], 12);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap'
}).addTo(map);


const coordinates = {
    0: [51.098161, 71.409690],
    1: [51.1894, 71.4591],
    2: [51.2094, 71.4691],
    3: [51.2294, 71.4791],
    4: [51.2494, 71.4891],
    5: [51.2694, 71.4991],
    6: [51.2894, 71.5091],
};

document.getElementById('predictButton').addEventListener('click', function() {
    let arrivalHour = document.getElementById('arrival_hour').value;
    let arrivalWeekday = document.getElementById('arrival_weekday').value;
    let dwellTime = document.getElementById('dwell_time_in_seconds').value;

    fetch('http://127.0.0.1:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            arrival_hour: arrivalHour,
            arrival_weekday: arrivalWeekday,
            dwell_time_in_seconds: dwellTime
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = `Предсказанное время прибытия: ${data.predicted_arrival}`;


        const coords = coordinates[arrivalWeekday];
        if (coords) {

            map.eachLayer(layer => {
                if (layer instanceof L.Marker) {
                    map.removeLayer(layer);
                }
            });


            L.marker(coords).addTo(map)
                .bindPopup(`Предсказанное время: ${data.predicted_arrival}`)
                .openPopup();
        }
    })
    .catch(error => console.error('Ошибка:', error));
});
