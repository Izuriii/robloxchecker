import requests
import time
from datetime import datetime
from termcolor import colored

# ===== IZURI LOGO =====
IZURI_LOGO = r"""
██╗███████╗██╗░░██╗██████╗░██╗
██║╚══███╔╝██║░░██║██╔══██╗██║
██║░░███╔╝░██║░░██║██████╔╝██║
██║░███╔╝░░██║░░██║██╔══██╗██║
██║███████╗╚██████╔╝██║░░██║██║
╚═╝╚══════╝░╚═════╝░╚═╝░░╚═╝╚═╝

"""

print(colored(IZURI_LOGO, "cyan", attrs=["bold"]))
print(colored("            Izuri Roblox Checker\n", "yellow", attrs=["bold"]))


# ===== DATE FORMATTER =====
def parse_date(date_str):
    if not date_str:
        return "Unknown Date"

    formats = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except:
            pass
    return "Unknown Date"


# ===== ROBLOX FETCHER =====
def get_roblox_user_info(username, password):
    try:
        # get user id
        lookup = requests.post(
            "https://users.roblox.com/v1/usernames/users",
            json={"usernames": [username]},
            timeout=10
        )

        data = lookup.json().get("data")
        if not data:
            print(colored(f"❌ User not found: {username}", "red"))
            return None

        user_id = data[0]["id"]

        # basic profile
        profile = requests.get(f"https://users.roblox.com/v1/users/{user_id}", timeout=10).json()
        friends = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/friends/count", timeout=10).json().get("count", 0)
        followers = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/followers/count", timeout=10).json().get("count", 0)
        badges = requests.get(f"https://badges.roblox.com/v1/users/{user_id}/badges?limit=100", timeout=10).json().get("data", [])
        groups = requests.get(f"https://groups.roblox.com/v1/users/{user_id}/groups/roles", timeout=10).json().get("data", [])
        collectibles = requests.get(f"https://inventory.roblox.com/v1/users/{user_id}/assets/collectibles?limit=10", timeout=10).json().get("data", [])

        avatar = f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=150x150&format=Png"

        return {
            "USER": username,
            "PASS": password,
            "UserID": user_id,
            "Username": profile.get("name"),
            "DisplayName": profile.get("displayName"),
            "ProfileURL": f"https://www.roblox.com/users/{user_id}/profile",
            "Description": profile.get("description", "N/A"),
            "IsBanned": profile.get("isBanned", False),
            "AccountAgeDays": profile.get("age"),
            "JoinDate": parse_date(profile.get("created")),
            "BadgeCount": len(badges),
            "CollectibleCount": len(collectibles),
            "GroupCount": len(groups),
            "FriendCount": friends,
            "FollowerCount": followers,
            "Avatar": avatar
        }

    except Exception as e:
        print(colored(f"❌ Error fetching {username}: {e}", "red"))
        return None


# ===== LOAD FILE =====
file_name = input("Enter file name: ")

try:
    with open(file_name, "r") as file:
        lines = file.read().splitlines()

    accounts = []

    print(colored("\n🚀 Fetching data...\n", "yellow", attrs=["bold"]))

    for line in lines:
        if ":" not in line:
            print(colored(f"❌ Invalid format: {line}", "red"))
            continue

        username, password = line.split(":", 1)
        accounts.append((username.strip(), password.strip()))

    output_file = "izuri_roblox_results.txt"

    with open(output_file, "w") as f:
        f.write(IZURI_LOGO + "\n")
        f.write("            Created by IZURI\n\n")

        for i, (username, password) in enumerate(accounts, 1):
            print(colored(f"🔍 Checking {i}/{len(accounts)}: {username}", "yellow"))

            info = get_roblox_user_info(username, password)

            if not info:
                continue

            f.write("⪻━━━━━═『IZURI』═━━━━━⪼\n\n")

            for k, v in info.items():
                line = f"[+] {k}: {v}"
                f.write(line + "\n")
                print(colored(line, "green"))

            f.write("\n⪻━━━━━━━━━━━━━━━━━━━⪼\n\n")
            print(colored("⪻━━━━━━━━━━━━━━━━━━━⪼\n", "cyan"))

            time.sleep(0.3)

    print(colored(f"\n✅ Done! Saved to {output_file}", "green", attrs=["bold"]))

except FileNotFoundError:
    print(colored("❌ File not found!", "red"))
