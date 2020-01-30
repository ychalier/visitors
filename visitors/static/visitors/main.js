function sendRequest(url, callback) {
    let request = new XMLHttpRequest();
    request.onload = (event) => {
        let response = JSON.parse(event.target.responseText);
        callback(response);
    }
    request.open("GET", url, true);
    request.send();
}

sendRequest(VISITORS_API_URL + "?part=total", (response) => {
    document.getElementById("total_visits").innerHTML = response.total_visits;
    document.getElementById("total_visitors").innerHTML = response.total_visitors;
});

sendRequest(VISITORS_API_URL + "?part=traffic", (response) => {
    let canvas = document.getElementById("visits_linechart");
    let labels = [];
    let visitsData = [];
    let visitorsData = [];
    for (let date in response.traffic_visits) {
        labels.push(date);
        visitsData.push(response.traffic_visits[date]);
        visitorsData.push(response.traffic_visitors[date]);
    }
    let chart = new Chart(canvas, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                data: visitsData,
                label: "visits",
                borderColor: "#3e95cd",
                fill: false
            }, {
                data: visitorsData,
                label: "visitors",
                borderColor: "#3cba9f",
                fill: false
            }]
        },
    });
});

sendRequest(VISITORS_API_URL + "?part=paths", (response) => {
    let canvas = document.getElementById("paths_barchart");
    let labels = [];
    let visitsData = [];
    let visitorsData = [];
    response.visits_per_path.forEach((item, i) => {
        labels.push(item.path);
        visitsData.push(item.count);
        visitorsData.push(response.visitors_per_path[i].count);
    });
    let chart = new Chart(canvas, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: 'visits',
                data: visitsData,
                backgroundColor: '#3e95cd',
            }, {
                label: 'visitors',
                data: visitorsData,
                backgroundColor: '#3cba9f',
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }],
            }
        }
    });
});
