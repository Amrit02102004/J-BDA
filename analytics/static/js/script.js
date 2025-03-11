const BASE_URL = "http://127.0.0.1:8000/api";

// Upload File
function uploadFile() {
    let fileInput = document.getElementById("fileInput").files[0];
    let messageDiv = document.getElementById("uploadMessage");

    if (!fileInput) {
        messageDiv.textContent = "Please select a file to upload.";
        return;
    }

    let formData = new FormData();
    formData.append("file", fileInput);

    fetch(`${BASE_URL}/upload/`, {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log("Upload Response:", data);
        messageDiv.textContent = data.message || data.error || "Upload successful!";
    })
    .catch(error => {
        console.error("Error uploading file:", error);
        messageDiv.textContent = "Error uploading file. Please try again.";
    });
}

// Fetch Analysis Data
function fetchData(endpoint) {
    fetch(`${BASE_URL}/${endpoint}/`)
        .then(response => response.json())
        .then(data => {
            console.log(`API Response for ${endpoint}:`, data); // Debugging step

            if (!data || Object.keys(data).length === 0 || (Array.isArray(data) && data.length === 0)) {
                document.getElementById("results").innerHTML = "<p class='text-danger'>No data available.</p>";
                return;
            }

            if (endpoint === "overview" || endpoint === "basic-stats") {
                displayTable(data);
            } else if (endpoint === "correlation-analysis") {
                displayChart(data);
            } else {
                document.getElementById("results").innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
            }
        })
        .catch(error => {
            console.error(`Error fetching data for ${endpoint}:`, error);
            document.getElementById("results").innerHTML = "<p class='text-danger'>Error fetching data.</p>";
        });
}

// Display Data in Table
function displayTable(data) {
    console.log("Table Data:", data); // Debugging

    let tableHTML = "<table id='dataTable' class='display'><thead><tr>";
    
    let headers;
    if (Array.isArray(data) && data.length > 0) {
        headers = Object.keys(data[0]);
    } else if (typeof data === "object") {
        headers = Object.keys(data);
        data = [data]; // Convert object to array for uniformity
    } else {
        document.getElementById("results").innerHTML = "<p class='text-danger'>No table data available.</p>";
        return;
    }

    headers.forEach(header => {
        tableHTML += `<th>${header}</th>`;
    });

    tableHTML += "</tr></thead><tbody>";

    data.forEach(row => {
        tableHTML += "<tr>";
        headers.forEach(header => {
            tableHTML += `<td>${row[header] !== undefined ? row[header] : '-'}</td>`; // Handle missing values
        });
        tableHTML += "</tr>";
    });

    tableHTML += "</tbody></table>";

    document.getElementById("results").innerHTML = tableHTML;

    // Ensure DataTable is properly initialized
    setTimeout(() => {
        if ($.fn.DataTable.isDataTable("#dataTable")) {
            $("#dataTable").DataTable().destroy();
        }
        $("#dataTable").DataTable();
    }, 500);
}

// Display Data in Chart.js
let myChart; // Store chart instance globally
function displayChart(data) {
    console.log("API Response:", data); // Debugging - check API response

    const canvas = document.getElementById('correlationChart');
    
    if (!canvas) {
        console.error("Canvas element 'correlationChart' not found.");
        return;
    }

    const ctx = canvas.getContext('2d');
    if (!ctx) {
        console.error("Error: Could not get context for the chart.");
        return;
    }

    // Extract Labels (e.g., "K", "N", "P", "soil_moisture", etc.)
    const labels = Object.keys(data);
    
    // Extract correlation values (We pick a reference feature, e.g., "N")
    const referenceFeature = "N";  // Change this to any feature you want to compare
    const values = labels.map(label => data[label][referenceFeature]); // Extract correlations with "N"

    // Destroy existing chart if present (to prevent duplicate charts)
    if (window.myChart instanceof Chart) {
        window.myChart.destroy();
    }

    // Create new chart
    window.myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels, // Feature names
            datasets: [{
                label: `Correlation with ${referenceFeature}`,
                data: values, // Correlation values
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: false }
            }
        }
    });
}
