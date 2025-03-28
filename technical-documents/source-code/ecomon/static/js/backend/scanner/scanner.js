// Initialize the HTML5 QR Code scanner
// This script is used to initialize the HTML5 QR Code scanner and handle the scanning process.
let html5QrCode = new Html5Qrcode("reader");
let isScanning = false;
// Define the allowed URL pattern using a regular expression
const allowedPattern = /^https?:\/\/www\.ecomon\.org\.uk\/view-gym\/\d+$/;

// Function to handle the scanned URL (successful scan)
function onScanSuccess(decodedText, decodedResult) {
    console.log(`Scanned URL: ${decodedText}`, decodedResult);

    // Use requestAnimationFrame to avoid blocking
    requestAnimationFrame(() => {
        if (allowedPattern.test(decodedText)) {
            window.location.href = decodedText;
        } else {
            // Show non-blocking error notification
            showNonBlockingError("Invalid QR Code. Please scan a valid recycling gym QR code.");
        }
    });
}

// Create a non-blocking error display
function showNonBlockingError(message) {
    const errorDiv = document.getElementById('scanner-error');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    errorDiv.style.marginTop = '10px';
    errorDiv.style.color = 'red';
    errorDiv.style.fontWeight = 'bold';
    
    // Clear previous timeout if exists
    if (window.errorTimeout) clearTimeout(window.errorTimeout);
    
    // Hide after 2 seconds
    window.errorTimeout = setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 2000);
}

// Function to handle the scan failure
function onScanFailure(error) {
    console.warn(`Scan error: ${error}`);
}

// Function to start the scanner
function startScanner() {
    if (isScanning) return;
    
    // Use facingMode: "environment" for back camera
    html5QrCode.start(
        { facingMode: "environment" },
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
        alert("Unable to access camera. Please ensure permissions are granted.");
    });
}

// Function to stop the scanner
function stopScanner() {
    if (!isScanning) return;

    html5QrCode.stop().then(() => {
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

// Function to check if the uploaded file is a valid image
function isValidImage(file) {
    const validTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif'];
    return validTypes.includes(file.type);
}

// Add click handler for the file input label
document.querySelector('label[for="qr-input-file"]').addEventListener('click', function (e) {
    // Check if the scanner is running
    if (isScanning) {
        e.preventDefault();
        // Stop scanner and open file input
        stopScanner();
        setTimeout(() => {
            document.getElementById('qr-input-file').click();
        }, 100);
    }
});

// Updated file upload handler
document.getElementById("qr-input-file").addEventListener("change", function (e) {
    e.preventDefault();

    // Check if the file input is empty
    if (e.target.files.length === 0) return;

    // Get the uploaded file
    const fileInput = this;
    // Get the uploaded image file
    const imageFile = e.target.files[0];

    fileInput.value = "";

    // Check if the uploaded file is a valid image
    if (!isValidImage(imageFile)) {
        alert("Please upload a valid image (PNG, JPG, or JPEG only).");
        return;
    }

    html5QrCode.scanFile(imageFile, true)
        .then(decodedText => {
            // Directly use the scanned URL for redirection
            // Validate the scanned URL
            if (allowedPattern.test(decodedText)) {
                window.location.href = decodedText;
            } else {
                alert("Invalid QR Code. Please upload a valid recycling gym QR code.");
                console.warn("Scanned QR code does not match the expected format.");
            }
            // Hide the QR code canvas if it was scanning beforehand
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