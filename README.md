# Slack Bot with internet of things

This is a project of a slack bot, to automate your office/room/lab using some Raspberry Pi GPIO pins.

### Set up your slack workspace

Go to https://slack.com/ . First you'll need to create a new slack workspace to use in this project, or just get the API token from a existing workspace.
Then, go to https://my.slack.com/services/new/bot and choose a username for your bot.

After submit, we now have an API key. Copy this somewhere we'll need later.

![api key example](https://i.imgur.com/LPUquaF.png)

### Requirements

Now, on your Pi you'll need to install some dependencies:

 - Python3
 - pip3
 - python3-rpi.gpio

```
sudo apt-get install  python3 python3-pip python3-dev python3-rpi.gpio -y
```


And then some packages:

 - slackclient
 - psutil

```
pip3 install slackclient
```
```
pip3 install psutil
```



## Configuring the python file
Download the python file:
```
git clone https://github.com/vitor-veras/slackbot_iot.git
```

After downloading slackbot_iot.py file there's some things you'll need to adapt to your bot, like your API token that we generated earlier.

```
slack_client = SlackClient("your-api-token-here")
```

In this next step, we fetch our bot User ID. We will use this later to know when somebody is talking to our bot. We keep it in `slack_user_id`.

```
user_list = slack_client.api_call("users.list")  
for user in user_list.get('members'):  
    if user.get('name') == "your-bot-name":
        slack_user_id = user.get('id')
        break

```

###Personalize
Now you can personalize your bot with some GPIO pins(any doubts about GPIO pins go to [RPI.GPIO Documentation](https://pypi.python.org/pypi/RPi.GPIO)):
```
from slackclient import SlackClient
#GPIO SETUP
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(8,GPIO.OUT)

```

And some methods:
```
def lightOn():
    GPIO.output(8, 1)
    print ("light on!")
def lightOff():
    GPIO.output(8, 0)
    print ("light off!")
```

And then link the methods you've created to the bot's matching text part.
```
if re.match(r'.*(light off).*', message_text, re.IGNORECASE):
//words you want your bot to recognize
	lightOff() //the gpio method to execute
	slack_client.api_call(
	"chat.postMessage",
	channel=message['channel'],
	text="Light off!", //bot response
	as_user=True)
```
#Now, run it!
![yeeeeah](https://i.imgur.com/mvKbycf.png)

### Physical gpio setup example

This is an example configuration, of how you can use the GPIO pins to turn on a Led.

I'm using a Raspberry Pi B+ model 1 and the GPIO pins 6(Ground) and 8(GPIO). All the pins of this Raspberry that i'm using can be found in this picture:
![gpio-pin](https://www.raspberrypi.org/documentation/usage/gpio-plus-and-raspi2/images/physical-pin-numbers.png)

Now a picture of the physical setup:

`Raspberry Pi + relay board with a Led`

![setup1](https://i.imgur.com/vF5HTQF.jpg)

####More information about the relay board can be found on [relay-board](https://github.com/vitor-veras/relay_board.git)
## Links
Some useful links :)

http://blog.benjie.me/building-a-slack-bot-to-talk-with-a-raspberry-pi/

https://www.raspberrypi.org/documentation/usage/gpio-plus-and-raspi2/

https://www.digitalocean.com/community/tutorials/how-to-use-rsync-to-sync-local-and-remote-directories-on-a-vps

https://www.raspberrypi.org/documentation/remote-access/ssh/

## Author

* **Vitor Veras de Moura** - [GitHub](https://github.com/vitor-veras) - Email: vitorverasm@gmail.com

