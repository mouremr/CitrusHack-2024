import serial
import time
import requests

def run_serial_communication():
    while True:  # Main loop
        try:
            with serial.Serial('COM5', 9600, timeout=1) as ser:
                time.sleep(2)  # Initial connection wait

                locationDict = {
                    "Los Angeles, CA": [34.0549, 118.2426],
                    "Riverside, CA": [33.9806, 117.3755],
                    "Maricopa, AZ": [33.056702, -112.046656],
                    "Jefferson, CO":[39.3773, 105.8006],
                    "New York, NY": [40.7128, -74.0060],
                    "Lakewood, CO": [39.7047, -105.0814],
                    "Paradise, NV": [36.0972, -115.1467],
                    "Atlanta, GA": [33.7490, -84.3880],
                    "Bellevue, WA": [47.6101, -122.2015],
                    "Boston, MA": [42.3601, -71.0589],
                    "Chicago, IL": [41.8781, -87.6298]
                }

                url = "https://api.weather.gov/gridpoints/BOU/62,61/forecast"
                
                response = requests.get(url, headers={"User-Agent": "SendAPIViaSerial"})
                data = response.json()

                # Just grab the temperature and short forecast from the first period
                forecast = data['properties']['periods'][0]
                text = f"{forecast['name']}: {forecast['temperature']}°{forecast['temperatureUnit']} - {forecast['shortForecast']}"

                while True:  # Connection persistence loop
                    # Send text
                    print(f"Sending: {text}")
                    ser.write((text + "\n").encode())
                    ser.flush()
                    
                    # Receive response
                    response = ser.readline().decode().strip()
                    if response:
                        print(f"Arduino says: {response}")
                    else:
                        print("No response received")
                    
                    # Customize this delay as needed
                    time.sleep(3)  # 2-second interval between messages
                    
        except serial.SerialException as e:
            print(f"Connection error: {e}")
            print("Reconnecting in 5 seconds...")
            time.sleep(5)
        except KeyboardInterrupt:
            print("\nExiting program")
            break

if __name__ == "__main__":
    run_serial_communication()