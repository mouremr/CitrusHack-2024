import serial
import time
import requests

from ultralytics import YOLO
import cv2

orange_model = YOLO('C:/Users/doodl/OneDrive/Documents/PlatformIO/Projects/arduino_backend/runs/detect/train/weights/best.pt')
leaf_model = YOLO('C:/Users/doodl/OneDrive/Documents/PlatformIO/Projects/arduino_backend/runs/detect/train4/weights/best.pt')

cap = cv2.VideoCapture(0)  # 0 is usually the default webcam


def get_forecast(lat, lon, headers):
    try:
        point_url = f"https://api.weather.gov/points/{lat},{lon}"

        r = requests.get(point_url, headers = headers)
        r.raise_for_status()
        data = r.json()
        forecast_url = data["properties"]["forecastHourly"]

        forecast_response = requests.get(forecast_url, headers=headers)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()

        return forecast_data["properties"]["periods"][0]["shortForecast"]

    except Exception as e:
        return f"Error fetching forecast: {e}"
    

def get_temperature(lat, lon, headers):
    try:
        point_url = f"https://api.weather.gov/points/{lat},{lon}"
        r = requests.get(point_url, headers = headers)
        r.raise_for_status()
        data = r.json()
        forecast_url = data["properties"]["forecastHourly"]

        forecast_response = requests.get(forecast_url, headers=headers)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()

        return forecast_data["properties"]["periods"][0]["temperature"]

    except Exception as e:
        return f"Error fetching forecast: {e}"


aqi_token="866300026ed058c9c619e3c00e80a891358cb496"


def get_aqi(city):

    try:
        point_url = f"https://api.waqi.info/feed/{city}/?token={aqi_token}"
        r = requests.get(point_url )
        r.raise_for_status()
        data = r.json()
        return data["data"]["aqi"]

    except Exception as e:
        return f"Error fetching forecast: {e}"


def run_serial_communication():
    with serial.Serial('COM4', 9600, timeout=1) as ser:
        #time.sleep(0.5)  # Initial connection wait

        locationDict = {
            "Houston TX": [29.7499,  -95.3584],
            "Riverside CA": [33.9806, -117.3755],
            "Bakersfield CA": [35.3935, -119.0437],
            "Jefferson CO":[39.3773, -105.8006],
            "Phoenix AZ": [33.4483, -112.0740],
            "Fairbanks AK": [64.8353, -147.7767],
            "Knoxville TN": [35.9646, -83.9264],
            "Atlanta GA": [33.7490, -84.3880],
            "Bellevue WA": [47.6101, -122.2015],
            "Boston MA": [42.3601, -71.0589],
            "Chicago IL": [41.8781, -87.6298]
        }

    
        headers = {"User-Agent" : "my-weather-script"}
        for city, (lat, lon) in locationDict.items():
            # Send text
            print(f"\nForecast for: {city}")
            
            temperature = get_temperature(lat, lon, headers = headers)
            forecast = get_forecast(lat, lon, headers=headers)
            aqi = get_aqi(city.rsplit(' ', 1)[0])

            if isinstance(forecast, str):
                print(forecast)
            else:
                for period in forecast[:2]:
                    print(f"{period['name']}: {period['detailedForecast']}")
            print(city+","+forecast + "-" + str(temperature) + "+"+ str(aqi)+"\n")
                
            #write to serial
            ser.write((city+","+forecast + "-" + str(temperature) + "+"+ str(aqi)+"\n").encode())

            ser.flush()
            
          
            time.sleep(0.725) 

        while True:
            ret, frame = cap.read()

            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break

            orange_results = orange_model(frame)

            leaf_results =leaf_model(frame)
            
            orange_detected = False  # <-- Track orange per frame

            for result in orange_results:
                boxes = result.boxes  # Boxes object for bbox outputs
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    confidence = box.conf[0].item()
                    class_id = box.cls[0].item()

                    # Check if the detected object is an orange (adjust class ID if needed)
                    if class_id == 0 and confidence > 0.4:  # Assuming 'orange' class ID is 0
                        # Draw bounding box and label on the frame
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        label = f'Orange {confidence:.2f}'
                        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                        ser.write(("1\n").encode()) #it is an oran
                        orange_detected = True

                    else:
                        ser.write(("0\n").encode())
            
            if not orange_detected:
                ser.write(("0\n").encode())

            # for result in leaf_results:
            #     boxes = result.boxes  # Boxes object for bbox outputs
            #     for box in boxes:
            #         x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            #         confidence = box.conf[0].item()
            #         class_id = box.cls[0].item()

            #         # Check if the detected object is an leaf (adjust class ID if needed)
            #         if class_id == 0 and confidence > 0.7:  # Assuming 'leaf' class ID is 0
            #             # Draw bounding box and label on the frame
            #             cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            #             label = f'leaf {confidence:.2f}'
            #             cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            #             ser.write(("2\n").encode()) #it is a leaf
            #         else:
            #             ser.write(("0\n").encode())

            # Display the resulting frame
            cv2.imshow('Webcam', frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break        


if __name__ == "__main__":
    run_serial_communication()
