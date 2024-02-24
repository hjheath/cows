import argparse
import time
import subprocess

import requests
import schedule
import psutil

SERVER_URL = "http://127.0.0.1:5000"


def send_device_info(cow_name):
    battery_data = get_battery_info()
    data = {
        "timestamp": time.time(),
        "battery": battery_data,
        "username": current_user(),
    }
    response = requests.put(f"{SERVER_URL}/cows/{cow_name}", json=data)
    if response.status_code in [200, 201]:
        print(f"Sent data, response: {response.status_code}")
    else:
        print("API request failed!", response.status_code, response.text)


def get_battery_info():
    battery = psutil.sensors_battery()
    return {
        "plugged": battery.power_plugged,
        "percent": battery.percent,
        "time_remaining": (
            battery.secsleft
            if battery.secsleft != psutil.POWER_TIME_UNLIMITED
            else None
        ),
    }


def current_user():
    # Run the command to get the currently logged in user
    result = subprocess.run(
        ["/usr/bin/stat", "-f", "%Su", "/dev/console"], capture_output=True, text=True
    )
    logged_in_user = result.stdout.strip()
    return logged_in_user or None


def worker_ascii_art():
    return """
             __n__n__
      .------`-\00/-'
     /  ##  ## (oo)
    / \## __   ./
       |//YY \|/
       |||   |||
       Here I am!
    """


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to collect COW data")
    parser.add_argument("name", help="The name of this cow, e.g. buttercup")
    args = parser.parse_args()
    cow_name = args.name

    print(worker_ascii_art())

    # Schedule the job to run once a minute
    schedule.every().second.do(send_device_info, cow_name=cow_name)
    print(f"Starting scheduler for {cow_name}...")
    while True:
        schedule.run_pending()
        time.sleep(1)
