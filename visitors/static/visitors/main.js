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
        options: {
            scales: {
                xAxes: [{
                    ticks: {
                        autoSkip: true,
                        maxRotation: 90,
                        minRotation: 90
                    }
                }]
            }
        }
    });
});

sendRequest(VISITORS_API_URL + "?part=paths", (response) => {
    let canvas = document.getElementById("paths_barchart");
    let labels = [];
    let visitsData = [];
    let visitorsData = [];
    for (let item in response.visits_per_path) {
        labels.push(item);
    }
    labels.sort(function(a, b) {
        return response.visits_per_path[b] - response.visits_per_path[a];
    })
    labels.forEach((item, i) => {
        visitsData.push(response.visits_per_path[item]);
        visitorsData.push(response.visitors_per_path[item]);
    })
    let sliceEnd = 10;
    let chart = new Chart(canvas, {
        type: "bar",
        data: {
            labels: labels.slice(0, sliceEnd),
            datasets: [{
                label: 'visits',
                data: visitsData.slice(0, sliceEnd),
                backgroundColor: '#3e95cd',
            }, {
                label: 'visitors',
                data: visitorsData.slice(0, sliceEnd),
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
                xAxes: [{
                    ticks: {
                        autoSkip: false,
                        maxRotation: 90,
                        minRotation: 90,
                    },
                }],
            },
        }
    });
});

sendRequest(VISITORS_API_URL + "?part=group", (response) => {
    let canvas = document.getElementById("group_piechart");
    let labels = [];
    let visitsData = [];
    for (let group in response.visits_per_group) {
        labels.push(group);
        visitsData.push(response.visits_per_group[group]);
    }
    let chart = new Chart(canvas, {
        type: "doughnut",
        data: {
            datasets: [{
                data: visitsData
            }],
            labels: labels
        },
        options: {
            plugins: {
                colorschemes: {
                    scheme: "tableau.Tableau10"
                }
            }
        }
    });
});
