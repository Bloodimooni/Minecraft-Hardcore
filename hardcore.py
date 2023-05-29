import subprocess
import time
import os
import sys

usernames = []

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

while True:
    # Restart the Minecraft server
    print("\n" * 100)
    print("Starting minecraft server")
    # for LINUX SERVER
    minecraft_process = subprocess.Popen(["/bin/bash", "./run.sh"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,universal_newlines=True)
    
    # for Windows Server uncomment this line and make the line above a comment
    # minecraft_process = subprocess.Popen(["cmd","run.bat"],stdin=subprocess.PIPE, stdout=subprocess.PIPE,universal_newlines=True)

    print("Looking for deaths now...")

    # Function to check if a player has died
    def check_player_death():
        while True:
            line = minecraft_process.stdout.readline()
            out = line.replace("\n", "")
            print(out)
            if line.strip():
                if any(keyword in line for keyword in death_messages):
                    if not any(f"<{username}>" in line for username in usernames):
                        print("A player died")
                        minecraft_process.stdin.write(f"say {username} died, the server will restart with a new world.\n")
                        minecraft_process.stdin.flush()
                        time.sleep(10)
                        return
                elif " logged in with entity id" in line:
                    username = line.split("[")[2].split(": ")[1]
                    if username not in usernames:
                        usernames.append(username)
                        print(f"Username: {username} appended to list.")




    # Wait for a player to die
    try:
        check_player_death()
    except KeyboardInterrupt:
        print("\n\n\nKeyboardInterrupt: Stopping server...")
        minecraft_process.stdin.write("stop\n")
        minecraft_process.stdin.flush()
        time.sleep(5)
        minecraft_process.wait()
        sys.exit(0)
        


    # Wait for the server to shut down
    minecraft_process.stdin.write("stop\n")
    minecraft_process.stdin.flush()
    minecraft_process.wait()
    print("Server stopped.")

    # Delete the world directory
    # For Linux Server:
    os.system("rm -rf world/")

    # For Windows Server:
    #os.sytem("rmdir /s /q world")

    print("Directory world deleted.")
    time.sleep(1)
