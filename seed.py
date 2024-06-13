import requests
import time

# Function to make requests
def coday(url, headers):
    if url == "https://elb.seeddao.org/api/v1/seed/claim" or url == "https://elb.seeddao.org/api/v1/tasks/7fdc46b3-6612-453a-9ef7-05471800f0ad":
        response = requests.post(url, headers=headers)
    else:
        response = requests.get(url, headers=headers)
    return response.json()

# Banner ASCII Art
def print_banner():
    banner = """
  _________                 .___ __________        __    ___.           __________.__  _____ __   .__ 
 /   _____/ ____   ____   __| _/ \______   \ _____/  |_  \_ |__ ___.__. \______   \__|/ ____\  | _|__|
 \_____  \_/ __ \_/ __ \ / __ |   |    |  _//  _ \   __\  | __ <   |  |  |       _/  \   __\|  |/ /  |
 /        \  ___/\  ___// /_/ |   |    |   (  <_> )  |    | \_\ \___  |  |    |   \  ||  |  |    <|  |
/_______  /\___  >\___  >____ |   |______  /\____/|__|    |___  / ____|  |____|_  /__||__|  |__|_ \__|
        \/     \/     \/     \/          \/                   \/\/              \/               \/   
    """
    print(f"\033[1m\033[34m{banner}\033[0m")  # Bold and blue text

# Print banner at the start
print_banner()

# Read tokens from file
with open('data.txt', 'r') as file:
    tokens = [line.strip() for line in file if line.strip()]

# Define intervals in seconds
intervals = [15 * 60, 30 * 60]
interval_index = 0

while True:
    for index, token in enumerate(tokens):
        acc = index + 1
        headers = {
            "accept": "application/json, text/plain, */*",
            "origin": "https://cf.seeddao.org",
            "referer": "https://cf.seeddao.org/",
            "telegram-data": token
        }
        date = time.strftime('%d-%m-%Y %H:%M:%S')

        try:
            claim_response = coday("https://elb.seeddao.org/api/v1/seed/claim", headers)
            balance_response = coday("https://elb.seeddao.org/api/v1/profile/balance", headers)
            complete_task_response = coday("https://elb.seeddao.org/api/v1/tasks/7fdc46b3-6612-453a-9ef7-05471800f0ad", headers)
            jsC = claim_response
            jsB = balance_response
            jsT = complete_task_response
            complete_taskk_response = coday(f"https://elb.seeddao.org/api/v1/tasks/notification/{jsT['data']}", headers)

            if 'data' in jsC and jsC['data']['amount'] > 1:
                print(f"\033[32m[{date}] Account {acc}: success claim {jsC['data']['amount'] / 1000000000:.6f} [SEED Balance: {jsB['data'] / 1000000000:.6f}] \033[0m")
            elif 'message' in jsC:
                print(f"\033[31m[{date}] Account {acc}: {jsC['message']} [SEED Balance: {jsB['data'] / 1000000000:.6f}] \033[0m")
            else:
                print(f"\033[31m[{date}] Account {acc}: Unknown error [SEED Balance: {jsB['data'] / 1000000000:.6f}] \033[0m")

        except Exception as e:
            print(f"\033[31m[{date}] Account {acc}: Error occurred: {e} \033[0m")

    # Print wait message and wait for the next interval
    wait_time_minutes = intervals[interval_index] / 60
    print(f"\033[34m====[Wait {wait_time_minutes} minutes]====\033[0m")
    time.sleep(intervals[interval_index])

    # Update the interval index for alternating between 15 and 30 minutes
    interval_index = (interval_index + 1) % len(intervals)
