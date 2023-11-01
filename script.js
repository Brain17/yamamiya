document.addEventListener("DOMContentLoaded", function() {
    const cameraFeed = document.getElementById("camera");
    const detectButton = document.getElementById("detect-button");
    const resultsSection = document.getElementById("results");

    // Check for camera support
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices
            .getUserMedia({ video: true })
            .then(function(stream) {
                cameraFeed.srcObject = stream;
                cameraFeed.play();
            })
            .catch(function(error) {
                console.error("Error accessing camera:", error);
            });
    } else {
        console.error("Camera not supported by this browser.");
    }

    detectButton.addEventListener("click", function() {
        // Here, you can run the YOLO license plate detection code using an appropriate backend (Python or API).
        // Display the detection results in the 'resultsSection'.
        // You may need to make an API request to your Python code running on the server.

        // Example:
        // fetch("/detect-license-plates", {
        //     method: "POST",
        //     body: videoFrameData, // Send video frame data to your Python backend
        // })
        //     .then(response => response.json())
        //     .then(data => {
        //         // Process and display the license plate detection results
        //         resultsSection.innerHTML = JSON.stringify(data, null, 4);
        //     })
        //     .catch(error => {
        //         console.error("Error in license plate detection:", error);
        //     });
    });
});

