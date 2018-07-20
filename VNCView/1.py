import time
from vncdotool import api

client = api.connect('172.16.251.13', password='zhxg20181')
time.sleep(5)
client.captureScreen('screenshot.png')
# client.expectScreen('booted.png')
client.keyPress('enter')
# client.expectScreen('login_success.png', maxrms=10)
