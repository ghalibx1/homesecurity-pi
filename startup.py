import os

from os import system

# Main loop
def main():
    print("Starting intrusion detection script in background...")
    os.system("nohup python -u /home/pi/detection/detect.py > /dev/null 2>&1 &")

if __name__ == "__main__":
    main()
