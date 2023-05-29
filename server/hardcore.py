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
usernames = []
allowed_death_entities = [
    "Villager",
    "Cat",
    "Wolf",
    "Dog",
    "Horse",
    "Parrot"
]

death_messages = [
    "died",
    "drowned",
    "death",
    "experienced kinetic energy",
    "blew up",
    "blown up",
    "killed",
    "hit the ground too hard",
    "fell",
    "suffocated",
    "was slain",
    "burned to death",
    "tried to swim in lava",
    "got melted by a blaze",
    "failed to escape the Nether",
    "fell out of the world",
    "discovered the void",
    "discovered the floor was lava",
    "was doomed by the Wither",
    "got struck by lightning",
    "got caught in a trap",
    "was pricked to death",
    "got stung by a bee",
    "starved to death",
    "was doomed by a witch",
    "fell into a ravine",
    "was shot by a skeleton",
    "was blown off a cliff",
    "got suffocated in a wall",
    "was slain by a zombie"
]

# RIP Manu, he died for testing purposes

def enable_hardcore_mode():
    file_path = "server.properties"
    temp_file_path = "temp.properties"
    hardcore_key = "hardcore=false"
    hardcore_new = "hardcore=true"

    # Open the input file and create a temporary file for writing
    with open(file_path, "r") as input_file, open(temp_file_path, "w") as temp_file:
        # Read each line from the input file
        for line in input_file:
            # Check if the line contains the hardcore setting
            if line.strip() == hardcore_key:
                # Replace the line with the new value
                line = hardcore_new + "\n"
            # Write the modified or unchanged line to the temporary file
            temp_file.write(line)

    # Replace the original file with the temporary file
    os.replace(temp_file_path, file_path)
    print(GREEN + "[+]\tHardcore has been enabled in the server properties." + RESET)


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


def check_player_death():
        while True:
            line = minecraft_process.stdout.readline()
            out = line.replace("\n", "")
            print(YELLOW + out + RESET)
            if line.strip():
                if any(keyword in line for keyword in death_messages):
                    if not any(f"<{username}>" in line for username in usernames) \
                        and not any(death_entities in line for death_entities in allowed_death_entities):
                        for user in usernames:
                            if line.__contains__(user) == True:
                                dead_player = user
                            else:
                                continue

                        print(RED + "[-]\tA player died" + RESET)
                        minecraft_process.stdin.write(f"say {dead_player} died, the server will restart with a new world.\n")
                        minecraft_process.stdin.flush()
                        time.sleep(10)
                        return
                    
                elif " logged in with entity id" in line:
                    username = line.split("[")[2].split(": ")[1]
                    if username not in usernames:
                        usernames.append(username)
                        print(BLUE + f"[!]\tUsername: {username} appended to list." + RESET)

####    START   ####

# Check for the file first:
time.sleep(2)
print_banner()
check_and_create_run_file(operating_system)

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
    time.sleep(1)
