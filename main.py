import cv2
import torch
import numpy as np
from sort.sort import Sort
from util import get_car, read_license_plate, write_csv

# Check for GPU availability and set the device (use 'cuda' if you have a GPU)
device = torch.device("cpu")

results = {}
mot_tracker = Sort()

# Load models and move them to the GPU (Make sure to provide the correct paths to your YOLO model files)
coco_model = YOLO('yamamiya/yolov8n.pt', task='detect')
license_plate_detector = YOLO('yamamiya/plate.pt', task='detect')

# Load video (You should specify the video file or camera device index, e.g., 0 for the default camera)
cap = cv2.VideoCapture(0)  # Change 0 to your video file path or camera index
vehicles = [2, 3, 5, 7]

license_plate_numbers = {}

# Get the video frame dimensions and set up VideoWriter (This part needs corrections)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (frame_width, frame_height))

# Read frames
frame_nmr = -1
ret = True
while ret:
    frame_nmr += 1
    ret, frame = cap.read()
    if ret:
        results[frame_nmr] = {}
        # Detect vehicles
        detections = coco_model(frame)[0]
        detections_ = []
        for detection in detections.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = detection
            if int(class_id) in vehicles:
                detections_.append([x1, y1, x2, y2, score])

        # Track vehicles
        track_ids = mot_tracker.update(np.asarray(detections_))

        # Detect license plates
        license_plates = license_plate_detector(frame)[0]
        for license_plate in license_plates.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = license_plate

            # Assign license plate to car
            xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_ids)

            if car_id != -1:
                # Crop license plate
                license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]

                # Process license plate
                license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)

                # Read license plate number
                license_plate_text, license_plate_text_score = read_license_plate(license_plate_crop_thresh)

                if license_plate_text is not None:
                    results[frame_nmr][car_id] = {'car': {'bbox': [xcar1, ycar1, xcar2, ycar2]},
                                                  'license_plate': {'bbox': [x1, y1, x2, y2],
                                                                    'text': license_plate_text,
                                                                    'bbox_score': score,
                                                                    'text_score': license_plate_text_score}}
                    license_plate_numbers[car_id] = license_plate_text
                    print(f"Car ID {car_id}: License Plate Number: {license_plate_text}")

        # Draw bounding boxes and text on the frame
        for car_id, data in results[frame_nmr].items():
            car_bbox = data['car']['bbox']
            license_plate_bbox = data['license_plate']['bbox']
            text = data['license_plate']['text']

            cv2.rectangle(frame, (int(car_bbox[0]), int(car_bbox[1]), int(car_bbox[2]), int(car_bbox[3]), (0, 255, 0), 2)
            cv2.rectangle(frame, (int(license_plate_bbox[0]), int(license_plate_bbox[1]), int(license_plate_bbox[2]), int(license_plate_bbox[3]), (0, 0, 255), 2)
            cv2.putText(frame, text, (int(license_plate_bbox[0]), int(license_plate_bbox[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Write the frame to the output video (This part needs corrections)
        out.write(frame)

        # Display the current frame
        cv2.imshow('frame', frame)

        # Check for a key press and break the loop if the user presses 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the VideoWriter and capture objects (This part needs corrections)
out.release()
cap.release()
cv2.destroyAllWindows()

# Print the dictionary of license plate numbers
print("Detected License Plate Numbers:")
for car_id, plate_number in license_plate_numbers.items():
    print(f"Car ID {car_id}: License Plate Number: {plate_number}")
