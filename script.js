document.addEventListener("DOMContentLoaded", function() {
    const cameraFeed = document.getElementById("camera");
    const detectButton = document.getElementById("start-button");
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

    detectButton.addEventListener("click", function() {
        // You can add your license plate detection logic here and display the results in the 'resultsSection'.
    });
});
