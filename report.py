# -*- coding: utf-8 -*-

import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

import pickle
from pprint import pprint

SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']

API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'
CLIENT_SECRETS_FILE = 'client_secret.json'
def get_service():
  read_pickle = True
  write_pickle = False
  assert not (read_pickle and write_pickle)
  if read_pickle:
    with open('report_credentials.pickle', 'rb') as f:
      credentials = pickle.load(f)
  else:
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    if write_pickle:
      with open('report_credentials.pickle', 'wb') as f:
        pickle.dump(credentials, f)



  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def execute_api_request(client_library_function, **kwargs):
  response = client_library_function(
    **kwargs
  ).execute()

  return response

def analyze(response):
  total = 0
  for row in response['rows']:
    total += row[1]
  print(total)

if __name__ == '__main__':
  # Disable OAuthlib's HTTPs verification when running locally.
  # *DO NOT* leave this option enabled when running in production.
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

  youtubeAnalytics = get_service()
  response =  execute_api_request(
      youtubeAnalytics.reports().query,
      ids='channel==MINE',
      startDate='2023-07-17',
      endDate='2023-07-26',
      metrics='estimatedMinutesWatched,views,likes,subscribersGained',
      dimensions='day',
      sort='day'
  )
  pprint(response)
  analyze(response)
  
