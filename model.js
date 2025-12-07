async function predict() {
    let data = {
        FanHours: parseInt(document.getElementById("fan").value),
        ACHours: parseInt(document.getElementById("ac").value),
        RefHours: parseInt(document.getElementById("ref").value),
        TVHours: parseInt(document.getElementById("tv").value),
        MonitorHours: parseInt(document.getElementById("monitor").value),
        PumpHours: parseInt(document.getElementById("pump").value)
    };

    let response = await fetch("https://yourwebsite.com/predict", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    let result = await response.json();
    document.getElementById("result").innerHTML =
        "Estimated Electricity Bill: ₱" + result.bill;
}
