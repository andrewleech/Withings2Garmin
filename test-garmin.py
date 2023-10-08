#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import requests
import json
import argparse

from datetime import date
from datetime import datetime
import time

from garth.exc import GarthHTTPError
from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)
from optparse import OptionParser
from optparse import Option
from optparse import OptionValueError
from pathlib import Path

GARMIN_USERNAME = ""
GARMIN_PASSWORD = ""
tokenstore = "config/gtoken.json"

def main():

	global GARMIN_USERNAME, GARMIN_PASSWORD
	with open('config/secret.json') as secret_file:
		secret = json.load(secret_file)
		GARMIN_USERNAME = secret["user"]
		GARMIN_PASSWORD = secret["password"]

	usage = 'usage: test-garmin.py [options]'
	p = argparse.ArgumentParser(usage=usage)
	p.add_argument('--username', '--gu',  default=GARMIN_USERNAME, type=str, help='username to login Garmin Connect.')
	p.add_argument('--password', '--gp', default=GARMIN_PASSWORD, type=str, help='password to login Garmin Connect.')
	
	args = p.parse_args()
	test(args.username, args.password)  
		
      
def test(garmin_username, garmin_password):
      def verbose_print(s):
            sys.stdout.write(s)
      garmin = init_garmin(garmin_username, garmin_password, verbose_print)
      h = garmin.garth.connectapi("/userprofile-service/userprofile/user-settings")["userData"]["height"]
      print(h)
	

def init_garmin(garmin_username, garmin_password, verbose_print):
    """Initialize Garmin API with your credentials."""
    try:
        verbose_print(
            f"Trying to login to Garmin Connect using token data from '{tokenstore}'...\n"
        )
        garmin = Garmin()
        garmin.login(tokenstore)
    except (FileNotFoundError, GarthHTTPError, GarminConnectAuthenticationError):
        # Session is expired. You'll need to log in again
        verbose_print(
            "Login tokens not present, will login with your Garmin Connect credentials to generate them.\n"
            f"They will be stored in '{tokenstore}' for future use.\n"
        )
        try:
            garmin = Garmin(garmin_username, garmin_password)
            garmin.login()
            # Save tokens for next login
            garmin.garth.dump(tokenstore)

        except (
            FileNotFoundError,
            GarthHTTPError,
            GarminConnectAuthenticationError,
            requests.exceptions.HTTPError,
        ) as err:
            print(err)
            return None

    return garmin

if __name__ == '__main__':
	main()