import sys
import os
import logging
import wakeonlan

sys.path.append('../')

from samsungtvws import SamsungTVWS

logging.basicConfig(level=logging.INFO)

tv = SamsungTVWS('192.168.1.136') #replace with your samsung tv ip address if you want to trythis out :)

# Autosave token to file
token_file = os.path.dirname(os.path.realpath(__file__)) + '/tv-token.txt'
tv = SamsungTVWS(host='192.168.1.136', port=8002, token_file=token_file)  #replace host with tv ip address
#wakeonlan.send_magic_packet('54:bd:79:40:4d:7d')
# Toggle power
def power_on():
    tv.shortcuts().power()
    wakeonlan.send_magic_packet('54:bd:79:40:4d:7d')
    return

def open_hbo():
    #wakeonlan.send_magic_packet('54:bd:79:40:4d:7d')
    tv.run_app('3201601007230')
    return

def close_hbo():
    tv.rest_app_close('3201601007230')
    return

def vol_up(amount):
    tv.send_key("KEY_VOLUP", amount)
    return

def vol_down(amount):
    tv.send_key("KEY_VOLDOWN", amount)
    return

def enter():
    #wakeonlan.send_magic_packet('54:bd:79:40:4d:7d')
    tv.send_key("KEY_ENTER", 1)
    return

def back():
    tv.send_key("KEY_RETURN")
    return
def left(amount):
    tv.send_key("KEY_LEFT", amount)
    return

def right(amount):
    tv.send_key("KEY_RIGHT", amount)
    return

apps = tv.app_list()  #list apps on your tv
logging.info(apps)