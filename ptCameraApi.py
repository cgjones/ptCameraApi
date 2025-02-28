# Pan/Tilt Camera API
# Chris Jones

import requests
import json
import urllib
import time

# IP address and port used to communicate with the camera                 
camera_url = 'http://192.168.200.158:5000'

# Last commanded position of the camera
last_commanded_pos = [0,0]


# Set a different camera IP address and port programatically
# url - the camera IP address and port to set
def set_url(url):
	camera_url = url 


# Utility function that builds and sends a command to the camera
def send_command(command):
	url = camera_url + '/send_command'
	data = 'base -c ' + command
	headers = {'Content-Type': 'application/x-www-form-urlencoded'}
	response = requests.post(url, data='command=' + urllib.parse.quote(data), headers=headers)

	if 200 != response.status_code:
		print("command to pt camera failed: command_text" + command + ", status_code: " + str(response.status_code))
		return -1
	else:
		return 0


# Reset the camera hardware
# return - 0 for success, -1 for failure
def reset_camera():
	cmd_string = '{"T":600}'
	return send_command(cmd_string)


# Configure the from LED
# led - LED magnitude from 0 (OFF) to 255 (max)
# return - 0 for success, -1 for failure
def set_light(led):
	cmd_string = '{"T":132,"IO4":%s,"IO5":%s}' % (led,led)
	return send_command(cmd_string)


# Move the camera
# x - position along the X axis, centered at 0
# y - position along the Y axis, centered at 0
# return - 0 for success, -1 for failure
def move_camera(x, y):
	cmd_string = '{"T":133,"X":%s,"Y":%s}' % (x,y)
	rc = send_command(cmd_string)

	if rc is 0:
		last_commanded_pos[0] = x
		last_commanded_pos[1] = y

	return rc


# Get the last successfully commanded position of the camera
def get_last_commanded_pos():
	return last_commanded_pos


# List the names of pictures onboard the camera
# return - list of picture names
def list_onboard_pictures():
	url = camera_url + '/get_photo_names'
	response = requests.get(url)
	return response.text


# Clear any pictures stored onboard the camera
def clear_onboard_pictures():
	url = camera_url + '/delete_all_photos'
	response = requests.post(url)
	return response.text


# Take a picture with the camera
# return - filename of the picture on the camera
def take_picture():
	url = camera_url + '/take_picture'
	response = requests.post(url)
	return response.text.strip().replace('"','')


# Transfer a picture from the camera
# src_filename - filename of the picture on the camera to transfer
# dst_path - path at which to place the transferred picture
# return - 0 for success, -1 for failure
def transfer_picture(src_filename, dst_path):
	url = camera_url + "/pictures/" + src_filename 
	response = requests.get(url)
	if response.status_code == 200:
		with open(dst_path + "/" + src_filename, "wb") as file:
			file.write(response.content)
			return 0
	else:
			return -1
