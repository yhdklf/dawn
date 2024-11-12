import requests
import time
import urllib3
import json
from colorama import init, Fore, Style
from fake_useragent import UserAgent
import os

init(autoreset=True)

keepalive_url = "https://www.aeropres.in/chromeapi/dawn/v1/userreward/keepalive"
get_points_url = "https://www.aeropres.in/api/atom/v1/userreferral/getpoint"
extension_id = "fpdkjdnhkakefebpekbdhillbhonfjjp"
_v = "1.0.7"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ua = UserAgent()

def banner():
    os.system("title DAWN KEEP ALIVE" if os.name == "nt" else "clear")
    os.system("cls" if os.name == "nt" else "clear")

def display_welcome_message():
    print(r"""
       _ _                  _____    ___ 
      (_) |                |  _  |  /   |
  __ _ _| | __ _ _ __ __  _| |/' | / /| |
 / _` | | |/ _` | '_ \\ \/ /  /| |/ /_| |
| (_| | | | (_| | | | |>  <\ |_/ /\___  |
 \__, |_|_|\__,_|_| |_/_/\_\\___/     |_/
  __/ |                                  
 |___/ 
                                   
    """)

def read_accounts_from_json(filename="config.json"):
    try:
        with open(filename, 'r') as file:
            accounts = json.load(file)
        return accounts
    except FileNotFoundError:
        print(f"{Fore.RED}[X] Error: config file '{filename}' not found.{Style.RESET_ALL}")
        return []
    except json.JSONDecodeError:
        print(f"{Fore.RED}[X] Error: Invalid JSON format in '{filename}'.{Style.RESET_ALL}")
        return []

def get_total_points(headers):
    try:
        response = requests.get(get_points_url, headers=headers, verify=False)
        response.raise_for_status()

        json_response = response.json()
        if json_response.get("status"):
            reward_point_data = json_response["data"]["rewardPoint"]
            referral_point_data = json_response["data"]["referralPoint"]
            total_points = (
                reward_point_data.get("points", 0) +
                reward_point_data.get("registerpoints", 0) +
                reward_point_data.get("signinpoints", 0) +
                reward_point_data.get("twitter_x_id_points", 0) +
                reward_point_data.get("discordid_points", 0) +
                reward_point_data.get("telegramid_points", 0) +
                reward_point_data.get("bonus_points", 0) +
                referral_point_data.get("commission", 0)
            )
            return total_points
        else:
            print(f"{Fore.YELLOW}[!] Warning: {json_response.get('message', 'Unknown error when fetching points')}{Style.RESET_ALL}")
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}[X] Error fetching points: {e}{Style.RESET_ALL}")
    return 0

def make_keepalive_request(headers, email):
    keepalive_payload = {
        "username": email,
        "extensionid": extension_id,
        "numberoftabs": 0,
        "_v": _v
    }
    
    headers["User-Agent"] = ua.random 

    try:
        response = requests.post(keepalive_url, headers=headers, json=keepalive_payload, verify=False)
        response.raise_for_status()

        json_response = response.json()
        if 'message' in json_response:
            return True, json_response['message'] 
        else:
            return False, "Message not found in response"
    except requests.exceptions.RequestException as e:
        return False, str(e)  

def countdown(seconds):
    for i in range(seconds, 0, -1):
        print(f"{Fore.LIGHTBLUE_EX}[~] Restarting in: {i} seconds", end='\r')
        time.sleep(1)

def main():
    banner() 
    display_welcome_message()
    while True:
        accounts = read_accounts_from_json()
        if not accounts:
            break  

        total_accumulated_points = 0
        account_count = 1

        for account in accounts:
            email = account["email"]
            token = account["token"]
            headers = {
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "User-Agent": ua.random 
            }

            print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━[ Account {account_count} ]━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}[@] Email: {email}")

            points = get_total_points(headers)
            total_accumulated_points += points

            success, status_message = make_keepalive_request(headers, email)

            if success:
                print(f"{Fore.GREEN}[✓] Status: {status_message}")
                print(f"{Fore.YELLOW}[✓] Request for {email} successful.{Style.RESET_ALL}\n")
            else:
                print(f"{Fore.RED}[X] Error: {status_message}")
                print(f"{Fore.RED}[X] Request for {email} failed.{Style.RESET_ALL}\n")

            account_count += 1

        print(f"{Fore.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}")
        print(f"{Fore.MAGENTA}[@] All accounts processed.")
        print(f"{Fore.GREEN}[+] Total points from all users: {total_accumulated_points}")
        countdown(181)
        print(f"\n{Fore.GREEN}[✓] Restarting the process...{Style.RESET_ALL}\n")

if __name__ == "__main__":
    main()