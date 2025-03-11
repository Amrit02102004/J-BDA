const BASE_URL = "http://127.0.0.1:8000/api";

function uploadFile() {
    let fileInput = document.getElementById("fileInput").files[0];

    if (!fileInput) {
        document.getElementById("uploadMessage").textContent = "Please select a file to upload.";
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
        if (data.error) {
            document.getElementById("uploadMessage").innerHTML = `<span style="color: red;">${data.error}</span>`;
        } else {
            document.getElementById("uploadMessage").innerHTML = `<span style="color: green;">${data.message}</span>`;
        }
    })
    .catch(error => {
        console.error("Upload Error:", error);
        document.getElementById("uploadMessage").innerHTML = `<span style="color: red;">Upload failed. Please try again.</span>`;
    });
}

function fetchData(endpoint) {
    document.getElementById("results").innerHTML = `<p style="color: blue;">Fetching ${endpoint}...</p>`;

    fetch(`${BASE_URL}/${endpoint}/`)
    .then(response => {
        if (!response.ok) {
            throw new Error(`API request failed: ${response.status} ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        document.getElementById("results").innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
    })
    .catch(error => {
        console.error("Fetch Error:", error);
        document.getElementById("results").innerHTML = `<span style="color: red;">Error: ${error.message}</span>`;
    });
}
