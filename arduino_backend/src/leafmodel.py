from ultralytics import YOLO
import cv2

# Load the trained model
model = YOLO("yolov8n.pt")

model.train(
    data='C:/Users/doodl/OneDrive/Documents/PlatformIO/Projects/arduino_backend/src/leaf-count.v1i.yolov8/data.yaml',
    epochs=2,
    imgsz=640
)

# cap = cv2.VideoCapture(0)  # 0 is usually the default webcam

# while True:
#     # Read a frame from the webcam
#     ret, frame = cap.read()

#     if not ret:
#         print("Can't receive frame (stream end?). Exiting ...")
#         break

#     # Perform object detection
#     results = model(frame)

#     # Process the results
#     for result in results:
#         boxes = result.boxes  # Boxes object for bbox outputs
#         for box in boxes:
#             # Extract bounding box information
#             x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
#             confidence = box.conf[0].item()
#             class_id = box.cls[0].item()

#             # Check if the detected object is an orange (adjust class ID if needed)
#             if class_id == 0 and confidence > 0.2:  # Assuming 'orange' class ID is 0
#                 # Draw bounding box and label on the frame
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#                 label = f'Orange {confidence:.2f}'
#                 cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

#     # Display the resulting frame
#     cv2.imshow('Webcam', frame)

#     # Break the loop if 'q' is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release the webcam and close all windows
# cap.release()
# cv2.destroyAllWindows()


