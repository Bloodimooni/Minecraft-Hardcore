import subprocess
import time
import os
import sys
import platform

def print_banner():
    banner = """
██████╗ ██╗      ██████╗  ██████╗ ██████╗ ██╗███╗   ███╗ ██████╗  ██████╗ ███╗   ██╗██╗
██╔══██╗██║     ██╔═══██╗██╔═══██╗██╔══██╗██║████╗ ████║██╔═══██╗██╔═══██╗████╗  ██║██║
██████╔╝██║     ██║   ██║██║   ██║██║  ██║██║██╔████╔██║██║   ██║██║   ██║██╔██╗ ██║██║
██╔══██╗██║     ██║   ██║██║   ██║██║  ██║██║██║╚██╔╝██║██║   ██║██║   ██║██║╚██╗██║██║
██████╔╝███████╗╚██████╔╝╚██████╔╝██████╔╝██║██║ ╚═╝ ██║╚██████╔╝╚██████╔╝██║ ╚████║██║
╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝ ╚═╝╚═╝     ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝╚═╝
"""
    print("\n"*100)
    print(RED + "\tCreated by:\n" + banner + RESET)

## Colors

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"
FIRSTRUN = False

operating_system = platform.system()

allowed_death_entities = [
    "Named entity class",
    "entity class",
    "class_1646",
    "*"
]

death_messages = [
    "died",
    "drowned",
    "death",
    "experienced kinetic energy",
    "intentional game design",
    "blew up",
    "pummeled",
    "blown up",
    "killed",
    "hit the ground too hard",
    "fell",
    "left the confines of this world",
    "squished",
    "suffocated",
    "was burnt",
    "cactus",
    "was slain",
    "was shot",
    "burned to death",
    "tried to swim in lava",
    "got melted by a blaze",
    "failed to escape the Nether",
    "fell out of the world",
    "withered away",
    "discovered the void",
    "discovered the floor was lava",
    "was doomed by the Wither",
    "got struck by lightning",
    "got caught in a trap",
    "was pricked to death",
    "got stung by a bee",
    "was stung to death",
    "stung",
    "doomed to fall",
    "starved to death",
    "was doomed by a witch",
    "fell into a ravine",
    "was fireballed",
    "was shot by a Skeleton",
    "was blown off a cliff",
    "got suffocated in a wall",
    "was slain by a zombie",
    "was struck by lightning",
    "impaled",
    "squashed",
    "went up in flames",
    "flames",
    "didn't want to live",
    "skewered",
    "walked into fire",
    "went off with a bang",
    "walked into the danger zone",
    "was killed by magic",
    "froze to death",
    "was fireballed",
    "obliterated",
    "starved"
]

# RIP Manu, he died for testing purposes

def enable_hardcore_mode():
    file_path = "server.properties"
    temp_file_path = "temp.properties"
    hardcore_key = "hardcore=false"
    hardcore_new = "hardcore=true"

    with open(file_path, "r") as input_file, open(temp_file_path, "w") as temp_file:
        for line in input_file:
            if line.strip() == hardcore_key:
                line = hardcore_new + "\n"
            temp_file.write(line)

    # Replace the original file with the temporary file
    os.replace(temp_file_path, file_path)
    print(GREEN + "[+]\tHardcore has been enabled in the server properties." + RESET)

def check_eula_agreement():
    try:
        with open("eula.txt", "r") as file:
            for line in file:
                if line.strip() == "eula=true":
                    return True
        return False
    except FileNotFoundError:
        return False


def check_and_create_run_file(operating_system):
    if operating_system == "Linux":
        run_file_path = "./run.sh"
        run_file_content = "java -Xmx2048M -Xms1024M -jar server.jar nogui"
    elif operating_system == "Windows":
        run_file_path = "run.bat"
        run_file_content = "java -Xmx2048M -Xms1024M -jar server.jar nogui"
    else:
        print(RED + "[!]\tUnsupported operating system." + RESET)
        return

    try:
        with open(run_file_path, "r"):
            # Run file exists, no need to create
            return
    except FileNotFoundError:
        # Run file does not exist, create it
        with open(run_file_path, "w") as run_file:
            run_file.write(run_file_content)
        print(GREEN + f"[+]\t{run_file_path} created successfully." + RESET)         

def sum_of_deaths(deaths : dict):
    attempt_number = 1
    for i in deaths:
        attempt_number += deaths[i]
    return attempt_number 


def read_stats_from_file():
    stats = {}
    try:
        with open("stats","r") as file:
            out = file.read().replace("{","").replace("}","").replace("'","").split(",")
            for item in out:
                item = item.strip()
                key, value = item.split(":")
                key = key.strip()
                value = int(value.strip())
                stats[key] = value

            return stats

    except FileNotFoundError:
        return stats

def save_stats_to_file(stats):
    with open("stats","w") as file:
        file.write(str(stats))

def player_died(player):
    print(RED + "[-]\tA player died" + RESET)
    minecraft_process.stdin.write(f"say {player} died, the server will restart with a new world.\n")
    minecraft_process.stdin.flush()
    time.sleep(1)
    print(RED + f"[-]\t{deaths}" + RESET)
    minecraft_process.stdin.write(f"say Here are the stats: {deaths}\n")
    minecraft_process.stdin.flush()
    time.sleep(5)
    return


def line_contains_two_users(line):
    user_line_list = []
    for user in usernames:
        if user in line:
            user_line_list.append(user)
    
    if len(user_line_list) > 1:
        return True
    else:
        return False
            

def check_player_death():
        while True:
            line = minecraft_process.stdout.readline()
            out = line.replace("\n", "")
            print(YELLOW + out + RESET)
            if line.strip():

                if any(username in line for username in usernames):
                    
                    if any(keyword in line for keyword in death_messages):
                        
                        if not any(f"<{username}>" in line for username in usernames) \
                            and not any(death_entities in line for death_entities in allowed_death_entities):
                            
                            for user in usernames:                         
                                if line.__contains__(user) == True:
                                    if line_contains_two_users(line) == True:
                                        line = line.split(" was")
                                        line = line[0].split(": ")
                                        dead_player = line[1]
                                    else:
                                        dead_player = user

                                    if dead_player in deaths:
                                        deaths[f"{dead_player}"] += 1
                                        print(RED + f"\n\n[!]\t{dead_player} got added a death to their counter" + RESET)
                                    else:
                                        deaths[f"{dead_player}"] = 1
                                    player_died(dead_player)
                                    return

                                else:
                                    continue
                    
                    elif "stats" in line.lower():
                        print(GREEN + "[i]\tuser asked for stats, sending them" + RESET)
                        minecraft_process.stdin.write(f"say Attempt {attempt_number}: {str(deaths).replace('{','').replace('}','')}\n")
                        minecraft_process.stdin.flush()

                elif " logged in with entity id" in line:
                    username = line.split("[")[2].split(": ")[1]
                    if username not in usernames:
                        usernames.append(username)
                        print(BLUE + f"[!]\tUsername: {username} appended to internal list." + RESET)
             
                                          
####    START   ####

print_banner()
usernames = []
print(BLUE + "[i]\tReading stats from file." + RESET)
deaths = read_stats_from_file()
attempt_number = sum_of_deaths(deaths)
print(GREEN + f"[i]\tThis is attempt number {attempt_number}."+ RESET)
time.sleep(2)

# Check for the file first:
check_and_create_run_file(operating_system)

if check_eula_agreement() == False:
    try:
        os.system("rm eula.txt")
    except:
        pass
    with open("eula.txt","w") as eula:
        eula.write("eula=true") 

try:
    enable_hardcore_mode()
except Exception:
    print(RED + "[!]\tFirst run detected!")
    FIRSTRUN = True

while True:
    # Restart the Minecraft server
    print(GREEN + "[+]\tStarting minecraft server\n\n\n" + RESET)
    
    # Determine the operating system
    if operating_system == "Linux":
        minecraft_command = ["/bin/bash", "./run.sh"]
        delete_command = "rm -rf world/"

    elif operating_system == "Windows":
        minecraft_command = ["run.bat"]
        delete_command = "rmdir /s /q world"
    
    else:
        print(RED + "[!]\tUnsupported operating system." + RESET)
        sys.exit(1)

    minecraft_process = subprocess.Popen(minecraft_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
    time.sleep(3)
    print(BLUE + "[SERVER@localhost]\tLooking for deaths now" + RESET)

    # Wait for a player to die
    try:
        check_player_death()
    except KeyboardInterrupt:
        print("\n\n" + RED + "[-]\tKeyboardInterrupt: Stopping server..." + RESET)
        minecraft_process.stdin.write("stop\n")
        minecraft_process.stdin.flush()
        time.sleep(5)
        minecraft_process.wait()
        sys.exit(0)

    # Wait for the server to shut down
    minecraft_process.stdin.write("stop\n")
    minecraft_process.stdin.flush()
    minecraft_process.wait()
    print(BLUE + "[-]\tServer stopped." + RESET)

    if FIRSTRUN == True:
        enable_hardcore_mode()
        FIRSTRUN = False

    # Delete the world directory
    os.system(delete_command)
    print(RED + "[!]\tDirectory 'world' deleted." + RESET)
    save_stats_to_file(deaths)
    print(RED + f"[i]\tSaved all the stats to file." + RESET)
    time.sleep(1)
