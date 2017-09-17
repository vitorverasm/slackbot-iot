import re
import json
import psutil
import RPi.GPIO as GPIO
import time
from slackclient import SlackClient

#GPIO SETUP(you can change for whatever you want)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
#gpio pins that i used, feel free to change
GPIO.setup(8,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)

#PUT YOUR SLACK API
slack_client = SlackClient("your-slack-api-here")


# Fetch your Bot's User ID
#PUT YOUR BOT'S NAME
user_list = slack_client.api_call("users.list")
for user in user_list.get('members'):
    if user.get('name') == "your-bot-name":
        slack_user_id = user.get('id')
        break
        
#functions to automate when message is called
#personalize
def lightOn():
    GPIO.output(8, 1)
    print ("light on!")
def lightOff():
    GPIO.output(8, 0)
    print ("light off!")
def fanOn():
    GPIO.output(16, 1)
    print ("fan on!")
def fanOff():
    GPIO.output(16, 0)
    print ("fan off!")
def alarmOn():
    GPIO.output(22, 1)
    print ("alarm on!")
def alarmOff():
    GPIO.output(22, 0)
    print ("alarm off!")
# Start connection
if slack_client.rtm_connect():
    print ("Connected!")
    #matching messages
    while True:
        for message in slack_client.rtm_read():
            if 'text' in message and message['text'].startswith("<@%s>" % slack_user_id):

                print ("Message received: %s" % json.dumps(message, indent=2))

                message_text = message['text'].\
                    split("<@%s>" % slack_user_id)[1].\
                    strip()

                if re.match(r'.*(cpu).*', message_text, re.IGNORECASE):
                    cpu_pct = psutil.cpu_percent(interval=1, percpu=False)

                    slack_client.api_call(
                        "chat.postMessage",
                        channel=message['channel'],
                        text="My CPU is at %s%%." % cpu_pct,
                        as_user=True)

                if re.match(r'.*(memory|ram).*', message_text, re.IGNORECASE):
                    mem = psutil.virtual_memory()
                    mem_pct = mem.percent

                    slack_client.api_call(
                        "chat.postMessage",
                        channel=message['channel'],
                        text="My RAM is at %s%%." % mem_pct,
                        as_user=True)

                if re.match(r'.*(light on).*', message_text, re.IGNORECASE):
                    lightOn()
                    slack_client.api_call(
                        "chat.postMessage",
                        channel=message['channel'],
                        text="Light on!",
                        as_user=True)
                if re.match(r'.*(light off).*', message_text, re.IGNORECASE):
                    lightOff()
                    slack_client.api_call(
                        "chat.postMessage",
                        channel=message['channel'],
                        text="Light off!",
                        as_user=True)
                if re.match(r'.*(fan on).*', message_text, re.IGNORECASE):
                    fanOn()
                    slack_client.api_call(
                        "chat.postMessage",
                        channel=message['channel'],
                        text="Fan on!",
                        as_user=True)
                if re.match(r'.*(fan off).*', message_text, re.IGNORECASE):
                    fanOff()
                    slack_client.api_call(
                        "chat.postMessage",
                        channel=message['channel'],
                        text="Fan off!",
                        as_user=True)
                if re.match(r'.*(alarm on).*', message_text, re.IGNORECASE):
                    alarmOn()
                    slack_client.api_call(
                        "chat.postMessage",
                        channel=message['channel'],
                        text="Alarm on!",
                        as_user=True)
                if re.match(r'.*(alarm off).*', message_text, re.IGNORECASE):
                    alarmOff()
                    slack_client.api_call(
                        "chat.postMessage",
                        channel=message['channel'],
                        text="Alarm off!",
                        as_user=True)
        time.sleep(1)
