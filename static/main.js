// main.js

const convertBtn = document.querySelector("#convertBtn");
const downloadBtn = document.querySelector("#downloadBtn");
var filename;
downloadBtn.disabled = true;

const handleFormSubmission = () => {
    var form = document.getElementById('uploadForm');

    fetch('/convert', {
        method: 'POST',
        body: new FormData(form),
    })
    .then(response => response.json())
    .then(data => {
        filename = data.zip_filename;
        if (filename) {
            alert("Processing Completed. Now you can download the processed files")
            downloadBtn.disabled = false;
            form.reset();
        }
    })
    .catch(error => {
        alert("Some Error Occurred. Please Retry.")
        console.error('Error:', error);
    });
}

const downloadFile = () => {
    if (!filename) {
        console.error('Filename is not available.');
        return;
    }

    fetch(`/download`)
        .then(response => response.blob())
        .then(blob => {
            const blobUrl = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = blobUrl;
            link.download = 'output.zip';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(blobUrl);
            downloadBtn.disabled = true;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

const validateForm = () => {
    var fileInput = document.getElementById('fileInput');
    
    if (fileInput.files.length === 0) {
        alert('Please select at least one file.');
        return false;
    }
    return true;
}

downloadBtn.addEventListener("click", (e) => {
    e.preventDefault();
    downloadFile();
});

convertBtn.addEventListener("click", (e) => {
    e.preventDefault();
    if (validateForm()) {
        handleFormSubmission();
    }
})
