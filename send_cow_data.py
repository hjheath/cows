import argparse
import time
import subprocess

import requests
import schedule
import psutil



def send_device_info(cow_name):
    battery_data = get_battery_info()
    data = {
        "timestamp": int(time.time()),  # Unix timestamp in seconds
        "name": cow_name,
        "battery": battery_data,
        "user": current_user(),
    }
    response = requests.post('http://127.0.0.1:5000/device_info', json=data)
    print("Sending device data to server", data)
    if response.status_code == 200:
        print("Data sent successfully")
    else:
        print("API request failed")
        print(response.status_code, response.text)

def get_battery_info():
    battery = psutil.sensors_battery()
    return {
        "plugged": battery.power_plugged,
        "percent": battery.percent,
        "time_left": battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else None,
    }

def current_user():
    # Run the command to get the currently logged in user
    result = subprocess.run(['/usr/bin/stat', '-f', '%Su', '/dev/console'], capture_output=True, text=True)
    logged_in_user = result.stdout.strip()
    return logged_in_user or None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to collect COW data")
    parser.add_argument("name", help="The name of this cow, e.g. buttercup")
    args = parser.parse_args()

    cow_name = args.name
    print("Name provided:", cow_name)

    # Schedule the job to run once a minute
    schedule.every().second.do(send_device_info, cow_name=cow_name)

    print("Starting scheduler")
    while True:
        schedule.run_pending()
        time.sleep(1)
