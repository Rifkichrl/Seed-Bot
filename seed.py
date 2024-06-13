import requests
import json
import time

# Function to make requests
def coday(url, headers):
    if url == "https://elb.seeddao.org/api/v1/seed/claim" or url == "https://elb.seeddao.org/api/v1/tasks/7fdc46b3-6612-453a-9ef7-05471800f0ad":
        response = requests.post(url, headers=headers)
    else:
        response = requests.get(url, headers=headers)
    return response.json()

# Read tokens from file
with open('data.txt', 'r') as file:
    tokens = [line.strip() for line in file if line.strip()]

# Initial interval in seconds
intervals = [30 * 60, 60 * 60, 2 * 60 * 60, 3 * 60 * 60]
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

    print(f"\033[34m====[Wait {intervals[interval_index] / 60:.0f} minutes]====\033[0m")
    time.sleep(intervals[interval_index])

    # Update the interval index
    interval_index = (interval_index + 1) % len(intervals)
