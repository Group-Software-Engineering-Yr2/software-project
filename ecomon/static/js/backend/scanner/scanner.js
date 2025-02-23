let html5QrCode = new Html5Qrcode("reader");
let isScanning = false;

function onScanSuccess(decodedText, decodedResult) {
    console.log(`Scanned URL: ${decodedText}`, decodedResult);
    // Directly use the scanned URL for redirection
    window.location.href = decodedText;
}

function onScanFailure(error) {
    console.warn(`Scan error: ${error}`);
}

function startScanner() {
    if (isScanning) return;

    Html5Qrcode.getCameras().then(devices => {
        if (devices && devices.length) {
            const cameraId = devices[0].id;
            html5QrCode.start(
                cameraId,
                { fps: 10, qrbox: { width: 250, height: 250 } },
                onScanSuccess,
                onScanFailure
            ).then(() => {
                isScanning = true;
                document.getElementById("logo-and-text").style.display = "none";
                document.getElementById("start-scanner").style.display = "none";
                document.getElementById("content").style.marginTop = "20px";
                document.getElementById("teams").style.display = "none";
                document.getElementById("stop-scanner").style.display = "block";
                document.querySelector(".title").style.marginTop = "155px";
            }).catch(err => {
                console.error("Failed to start scanner:", err);
            });
        }
    }).catch(err => {
        console.error("Failed to get cameras:", err);
    });
}

function stopScanner() {
    if (!isScanning) return;

    html5QrCode.stop().then(() => {
        console.log("Scanner stopped.");
        isScanning = false;
        document.getElementById("logo-and-text").style.display = "block";
        document.getElementById("start-scanner").style.display = "block";
        document.getElementById("teams").style.display = "flex";
        document.getElementById("content").style.marginTop = "220px";
        document.getElementById("stop-scanner").style.display = "none";
        document.querySelector(".title").style.marginTop = "0";
    }).catch(err => {
        console.error("Failed to stop scanner:", err);
    });
}

function isValidImage(file) {
    const validTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif'];
    return validTypes.includes(file.type);
}

// Add click handler for the file input label
document.querySelector('label[for="qr-input-file"]').addEventListener('click', function(e) {
    if (isScanning) {
        e.preventDefault();
        stopScanner();
        setTimeout(() => {
            document.getElementById('qr-input-file').click();
        }, 100);
    }
});

// Updated file upload handler
document.getElementById("qr-input-file").addEventListener("change", function(e) {
    e.preventDefault();
    
    if (e.target.files.length === 0) return;
    
    const fileInput = this;
    const imageFile = e.target.files[0];
    
    fileInput.value = "";
    
    if (!isValidImage(imageFile)) {
        alert("Please upload a valid image (PNG, JPG, or JPEG only).");
        return;
    }
    
    html5QrCode.scanFile(imageFile, true)
        .then(decodedText => {
            console.log("File scanned successfully:", decodedText);
            // Directly use the scanned URL for redirection
            window.location.href = decodedText;
            if (document.getElementById("qr-canvas-visible")) {
                document.getElementById("qr-canvas-visible").style.display = "none";
            }
        })
        .catch(err => {
            console.error("Error scanning file:", err);
            alert("QR Code Not Found");
            if (document.getElementById("qr-canvas-visible")) {
                document.getElementById("qr-canvas-visible").style.display = "none";
            }
        });
});

document.getElementById("start-scanner").addEventListener("click", startScanner);
document.getElementById("stop-scanner").addEventListener("click", stopScanner);