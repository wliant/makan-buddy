# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 22:03:36 2020

@author: darry
"""

# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START calendar_quickstart]
from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def schedule_reservation(reservation_date,reservation_time,party_size,restaurant_name,first_name,restaurant_address):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow()

    reservation_day=reservation_date.split('/')[0]
    reservation_month =reservation_date.split('/')[1]
    reservation_year =reservation_date.split('/')[2]
    reservation_date = reservation_year+'-'+reservation_month+'-'+reservation_day
    start_time_hr= reservation_time[:2]
    end_time_hr= int(reservation_time[:2])+4
    start_time_min= reservation_time[2:]
    end_time_min=start_time_min
        
        
    event = {
      'summary': 'Reservation at '+restaurant_name,
      'location': restaurant_address,
      'description': 'Reservation for '+party_size+' under '+first_name+' made on '+str(now),
      'start': {
        'dateTime': reservation_date+'T'+start_time_hr+':'+start_time_min+':00+08:00',
        'timeZone': 'Asia/Singapore',
      },
      'end': {
        'dateTime': reservation_date+'T'+str(end_time_hr)+':'+end_time_min+':00+08:00',
        'timeZone': 'Asia/Singapore',
      },
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print ('Event created: %s', (event.get('htmlLink')))

if __name__ == '__main__':
    sample_reservation_date = "14/06/2020"
    sample_reservation_time = "1900"
    sample_party_size = "2"
    sample_restaurant_name ='Ristorante Takada'
    sample_first_name = 'sam'
    sample_last_name='lee'
    sample_email_address = 'tangmeng1993@gmail.com'
    sample_phone_number = '82053356'
    sample_restaurant_address="356 Alexandra Road"
    schedule_reservation(sample_reservation_date,sample_reservation_time,sample_party_size,sample_restaurant_name,sample_first_name,sample_restaurant_address)
# [END calendar_quickstart]