function checkNews() {
    const text = document.getElementById("newsText").value;
    const result = document.getElementById("result");
    const entitiesBox = document.getElementById("entities");

    result.innerHTML = "";
    entitiesBox.innerHTML = "";

    if (text.trim().length === 0) {
        result.innerHTML = "Please enter news text.";
        result.style.color = "red";
        return;
    }

    fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ news: text })
    })
    .then(response => response.json())
    .then(data => {
        if (data.prediction === "FAKE") {
            result.innerHTML = "⚠️ This news may be fake!";
            result.style.color = "red";
        } else {
            result.innerHTML = "✅ This news seems real.";
            result.style.color = "green";
        }

        if (data.entities && data.entities.length > 0) {
            let html = "<ul>";
            data.entities.forEach(ent => {
                html += `<li>${ent[0]} : ${ent[1]}</li>`;
            });
            html += "</ul>";
            entitiesBox.innerHTML = html;
        }

    })
    .catch(error => {
        result.innerHTML = "Error checking news.";
        result.style.color = "orange";
        console.error(error);
    });
}
