#!/usr/bin/env python
import httplib
import argparse
import json
import datetime
import time

def get_valid_username():
	username = raw_input('Enter username: ')
	if not username:
		print("Please enter a valid username.")
		username = get_valid_username()
	return username

def main():
	argparser = argparse.ArgumentParser()
	argparser.add_argument("--name", "-n", help="Username", type=str)
	args = argparser.parse_args()

        print("MinecraftInspector v" + "1.0")
        print("Created by ~xgh69.")
        print("")
        
	username = ""
	uuid = ""
	if args.name:
		username = args.name
	else:
		username = get_valid_username()
	try:
		conn = httplib.HTTPSConnection("api.mojang.com")
		conn.request("GET", "https://api.mojang.com/users/profiles/minecraft/" + username + "?at=" + str(int(time.time())))
	except:
		print("Cannot connect to api.mojang.com.")
		exit(1)
	responseRaw = conn.getresponse().read()
	responseJson = None
	try:
		responseJson = json.loads(responseRaw)
	except:
		print(username + " (username) not found in mojang database.")
		exit(1)
	try:
		uuid = responseJson['id']
		username = responseJson['name']
	except:
		print("Error: " + responseJson['error'])
		print("Error Message: " + responseJson['errorMessage'])
		exit(1)
	conn.close()
	try:
		conn = httplib.HTTPSConnection("api.mojang.com")
		conn.request("GET", "https://api.mojang.com/user/profiles/" + uuid + "/names")
	except:
		print("Cannot connect to api.mojang.com.")
		exit(1)
	responseRaw = conn.getresponse().read()
	try:
		responseJson = json.loads(responseRaw)
	except:
		print(uuid + " (uuid) not found in mojang database.")
		exit(1)
	i = 0
        print("UUID: " + uuid)
	while True:
		try:
			if i == 0:
				try:
					if responseJson[i + 1]['name']:
						print("Registered name: " + responseJson[i]['name'])
				except:
					print(username + " not changed username.")
			else:
				date = datetime.datetime.fromtimestamp(float(responseJson[i]['changedToAt'])/1000).strftime("%Y-%m-%d %H:%M:%S")
				print("Name #" + str(i + 1) + ": " + responseJson[i]['name'] + " | changed: " + date)
		except:
			if i == 0:
				print(username + " changed username 0 times.")
			exit(0)
		i += 1

if __name__ == "__main__": main()
