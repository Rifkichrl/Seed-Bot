import requests
import time

# Function to make requests with retry logic
def coday(url, headers, retries=3):
    for attempt in range(retries):
        try:
            if url in ["https://elb.seeddao.org/api/v1/seed/claim", "https://elb.seeddao.org/api/v1/tasks/7fdc46b3-6612-453a-9ef7-05471800f0ad", "https://elb.seeddao.org/api/v1/worms", "https://elb.seeddao.org/api/v1/login-bonuses"]:
                response = requests.post(url, headers=headers)
            else:
                response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(5)  # Wait before retrying
            else:
                raise

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

# Track last collection times
last_collection_time = {
    "worms": 0,
    "login_bonus": 0,
    "profile": 0,
}
collection_interval = 24 * 60 * 60  # 24 hours in seconds

while True:
    current_time = time.time()
    
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
            profile_response = coday("https://elb.seeddao.org/api/v1/profile", headers)
            complete_task_response = coday("https://elb.seeddao.org/api/v1/tasks/7fdc46b3-6612-453a-9ef7-05471800f0ad", headers)
            jsC = claim_response
            jsB = balance_response
            jsP = profile_response
            jsT = complete_task_response
            complete_taskk_response = coday(f"https://elb.seeddao.org/api/v1/tasks/notification/{jsT['data']}", headers)

            if 'data' in jsC and jsC['data']['amount'] > 1:
                print(f"\033[32m[{date}] Account {acc}: success claim {jsC['data']['amount'] / 1000000000:.6f} [SEED Balance: {jsB['data'] / 1000000000:.6f}] \033[0m")
            elif 'message' in jsC:
                print(f"\033[31m[{date}] Account {acc}: {jsC['message']} [SEED Balance: {jsB['data'] / 1000000000:.6f}] \033[0m")
            else:
                print(f"\033[31m[{date}] Account {acc}: Unknown error [SEED Balance: {jsB['data'] / 1000000000:.6f}] \033[0m")

            # Collect worms if 24 hours have passed since the last collection
            if current_time - last_collection_time["worms"] > collection_interval:
                worms_response = coday("https://elb.seeddao.org/api/v1/worms", headers)
                jsW = worms_response
                if 'data' in jsW:
                    print(f"\033[32m[{date}] Account {acc}: success collect worms {jsW['data']} \033[0m")
                elif 'message' in jsW:
                    print(f"\033[31m[{date}] Account {acc}: {jsW['message']} \033[0m")
                else:
                    print(f"\033[31m[{date}] Account {acc}: Unknown error during worm collection \033[0m")
                
                last_collection_time["worms"] = current_time

            # Claim login bonus if 24 hours have passed since the last claim
            if current_time - last_collection_time["login_bonus"] > collection_interval:
                login_bonus_response = coday("https://elb.seeddao.org/api/v1/login-bonuses", headers)
                jsL = login_bonus_response
                if 'data' in jsL:
                    print(f"\033[32m[{date}] Account {acc}: success claim login bonus {jsL['data']} \033[0m")
                elif 'message' in jsL:
                    print(f"\033[31m[{date}] Account {acc}: {jsL['message']} \033[0m")
                else:
                    print(f"\033[31m[{date}] Account {acc}: Unknown error during login bonus claim \033[0m")
                
                last_collection_time["login_bonus"] = current_time

            # Collect profile info if 24 hours have passed since the last collection
            if current_time - last_collection_time["profile"] > collection_interval:
                profile_response = coday("https://elb.seeddao.org/api/v1/profile", headers)
                jsP = profile_response
                if 'data' in jsP:
                    print(f"\033[32m[{date}] Account {acc}: success collect profile info \033[0m")
                elif 'message' in jsP:
                    print(f"\033[31m[{date}] Account {acc}: {jsP['message']} \033[0m")
                else:
                    print(f"\033[31m[{date}] Account {acc}: Unknown error during profile info collection \033[0m")
                
                last_collection_time["profile"] = current_time

        except Exception as e:
            print(f"\033[31m[{date}] Account {acc}: Error occurred: {e} \033[0m")

    # Print wait message and wait for the next interval
    wait_time_minutes = intervals[interval_index] / 60
    print(f"\033[34m====[Wait {wait_time_minutes} minutes]====\033[0m")
    time.sleep(intervals[interval_index])

    # Update the interval index for alternating between 15 and 30 minutes
    interval_index = (interval_index + 1) % len(intervals)
