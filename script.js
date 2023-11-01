document.addEventListener("DOMContentLoaded", function() {
    const cameraFeed = document.getElementById("camera");
    const startButton = document.getElementById("start-button");
    const switchCameraButton = document.getElementById("switch-camera-button");
    const resultsSection = document.getElementById("results");
    let currentStream = null;

    // Function to start the camera feed
    function startCamera() {
        const constraints = {
            video: { facingMode: "environment" } // Use "user" for front camera
        };

        navigator.mediaDevices
            .getUserMedia(constraints)
            .then(function(stream) {
                currentStream = stream;
                cameraFeed.srcObject = stream;
                cameraFeed.play();
            })
            .catch(function(error) {
                console.error("Error accessing camera:", error);
            });
    }

    // Check for camera support
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        startCamera();
    } else {
        console.error("Camera not supported by this browser.");
    }

    // Switch camera button click event
    switchCameraButton.addEventListener("click", function() {
        if (currentStream) {
            currentStream.getTracks().forEach(function(track) {
                track.stop();
            });
        }
        startCamera();
    });

    startButton.addEventListener("click", function() {
        // Trigger license plate detection using Python code in main.py
        fetch("/detect-license-plates", {
            method: "POST",
            body: JSON.stringify({ command: "start_detection" }),
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            // Process and display the license plate detection results
            resultsSection.innerHTML = JSON.stringify(data, null, 4);
        })
        .catch(error => {
            console.error("Error in license plate detection:", error);
        });
    });
});
