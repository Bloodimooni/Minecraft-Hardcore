import os
import time
import platform
import sys

operating_system = platform.system()
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"

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

def install_jdk(operating_system):
    
    if operating_system == "Linux":
        jdk = "default-jdk"

        print(YELLOW + "[JAVA]\tPlease intall Java" + RESET)
        os.system(f"sudo apt install {jdk}")
    
    elif operating_system == "Windows":
        jdk = ".\\dependencies\\jdk-20_windows-x64_bin.exe"
        jre = ".\\dependencies\\jre-8u371-windows-x64.exe"

        print(YELLOW + "[JDK]\tPlease intall the Java JDK version" + RESET)
        os.system(jdk)
        print(YELLOW + "[JRE]\tPlease intall the Java JRE version" + RESET)
        os.system(jre)
        
    else:
        print(RED + "[!]\tUnsupported operating system." + RESET)
        sys.exit(1)

def eula_auto_accept():
    with open(".\\server\\eula.txt", "w") as eula:
        eula.write("eula=true")
    

print_banner()
print("\n"*5)
install_jdk(operating_system)
print(GREEN + "[i]\tAccepting the EULA for the minecraft server."+ RESET)
eula_auto_accept()
print(GREEN + "[✓]\tEverything should be installed and ready to go!"+ RESET)
time.sleep(5)
sys.exit(0)
