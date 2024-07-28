from twilio.rest import Client
import os
import keys
from os import system
import time
import re

# Configuration 

LOG_FILE = "/home/pi/detection/ssh_logs.log" # can add multiple
CHECK_INTERVAL = 60  # Check every 60 seconds
suspicious_activity = []

# Regular expressions for detecting suspicious activities
PATTERNS = [ 
    re.compile(r'Failed password for') # can add multiple
]

# Function to send an alert email
def send_alert(message):
	client = Client(keys.account_sid, keys.auth_token)
	text_message = client.messages.create(
		body=message,
		from_=keys.twilio_number,
		to=keys.my_phone_number
		)
    
# Function to check the log file for suspicious activities
def check_logs():
    with open(LOG_FILE, 'r') as file:
        lines = file.readlines()
        
    new_suspicious_activity = []
 
    for line in lines:
            for pattern in PATTERNS:
                if pattern.search(line):
                    if line not in suspicious_activity and line not in new_suspicious_activity:
                        suspicious_activity.append(line)
                        new_suspicious_activity.append(line)
    if new_suspicious_activity:
        send_alert("\n".join(new_suspicious_activity))

# Main loop
def main():
    print("Starting intrusion detection script...")   
    
    while True:
        os.system("journalctl -S '2 minute ago' -u ssh.service > /home/pi/detection/ssh_logs.log")
        check_logs()
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()