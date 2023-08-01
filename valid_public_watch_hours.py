import os

import pickle

from pprint import pprint

import subprocess

from datetime import datetime

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


def main():
    start_date = '2023-06-10'
    end_date = '2023-06-16'
    date_difference = calculate_date_difference(start_date, end_date)
    git_commit = subprocess.run(["git log | head -n 1"], stdout=subprocess.PIPE, text=True, shell=True).stdout
    output_file_path = f'output/stats_{datetime.now().strftime("%Y-%m-%d_%H:%M:%S").replace(":", "-")}.txt'
    add_to_stats_file(
        f"""start_date: {start_date}
end_date: {end_date}
git_commit: {git_commit}""",
        output_file_path
    )

    youtube = get_youtube()

    youtube_analytics = get_youtube_for_analytics()

    # do_test_thing(youtube_analytics)

    video_ids = get_all_video_ids_for_my_channel(youtube)
    add_to_stats_file(
        f'video_ids length: {len(video_ids)}',
        output_file_path
    )

    public_video_ids = filter_video_ids_to_public_videos_only(youtube, video_ids)
    add_to_stats_file(
        f'public_video_ids length: {len(public_video_ids)}',
        output_file_path
    )

    non_shorts_video_ids = filter_shorts_out_of_video_ids(youtube_analytics, public_video_ids)

    add_to_stats_file(
        f'length of non_shorts_video_ids: {len(non_shorts_video_ids)}',
        output_file_path
    )

    watch_minutes = calculate_watch_time(youtube_analytics, non_shorts_video_ids,  start_date, end_date)
    print(watch_minutes)
    add_to_stats_file(
        f'watch_minutes: {watch_minutes}',
        output_file_path
    )

    length_of_time_span = date_difference + 1
    yearly_projected_watch_minutes = watch_minutes * 365 / length_of_time_span
    yearly_projected_watch_hours = yearly_projected_watch_minutes / 60
    add_to_stats_file(
        f"""
Commentary:
At this pace, you would have {yearly_projected_watch_minutes} mminutes
in a year.
That's {yearly_projected_watch_hours} hours
""",
        output_file_path
    )


def calculate_date_difference(start_date: str, end_date: str) -> int:
    date_format = '%Y-%m-%d'

    try:
        start_date_obj = datetime.strptime(start_date, date_format)
        end_date_obj = datetime.strptime(end_date, date_format)
        difference = end_date_obj - start_date_obj
        return difference.days
    except ValueError as e:
        print("Error: ", e)
        return -1


def add_to_stats_file(s, file_path):
    with open(file_path, 'a') as f:
        f.write(s + '\n')

def calculate_watch_time(youtube_analytics, non_shorts_video_ids, start_date, end_date):
    total_watch_minutes = 0
    for video_id in non_shorts_video_ids:
        response = execute_analytics_api_request(
            youtube_analytics.reports().query,
            ids='channel==MINE',
            startDate=start_date,
            endDate=end_date,
            # dimensions="",
            # sort='day',
            metrics="estimatedMinutesWatched",
            filters=f'video=={video_id}'
        )
        total_watch_minutes += response['rows'][0][0]
        print(video_id, total_watch_minutes)
    return(total_watch_minutes)

def filter_shorts_out_of_video_ids(youtube_analytics, public_video_ids):
    non_shorts_video_ids = []
    for video_id in public_video_ids:
        response = execute_analytics_api_request(
            youtube_analytics.reports().query,
            ids='channel==MINE',
            startDate='2017-01-01',
            endDate='2023-12-31',
            dimensions="video,creatorContentType",
            # sort='day',
            metrics="views",
            filters=f'video=={video_id}'
        )
        if len(response['rows']) > 0:
            if response['rows'][0][1] == 'shorts':
                print(f'filter_shorts_out_of_video_ids: filtering out short, video_id: {video_id}')
                continue
            else:
                print(f'filter_shorts_out_of_video_ids: adding non-short video, video_id: {video_id}')
                non_shorts_video_ids.append(video_id)

        else:
            print(f'filter_shorts_out_of_video_ids: no information found for video_id: {video_id}')
    return non_shorts_video_ids


    return 'foo'

def get_youtube_for_analytics():
    API_SERVICE_NAME = 'youtubeAnalytics'
    API_VERSION = 'v2'
    CLIENT_SECRETS_FILE = 'client_secret.json'
    SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']

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

    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def execute_analytics_api_request(client_library_function, **kwargs):
  response = client_library_function(
    **kwargs
  ).execute()

  return response


def do_test_thing(youtube_analytics):
    video_id = 'he2JBiIaSrw'
    try:
        response = execute_analytics_api_request(
            youtube_analytics.reports().query,
            ids='channel==MINE',
            startDate='2017-01-01',
            endDate='2023-12-31',
            dimensions="video,creatorContentType",
            # sort='day',
            metrics="views",
            filters='video==_sIGf3YWUfA'
        )
        # video GWRYWyURn4Y, videoOnDemand
        # video Z82C8jPSIac, no rows
    except HttpError as e:
        print('erroar', e)

    pprint(response)
    print('hello')

    request = youtube_analytics.videos().list(
        part="status,snippet,contentDetails,statistics",
        id=video_id
    )
    response = request.execute()
    privacy_status = response['items'][0]['status']['privacyStatus']
    if privacy_status == 'public':
        pass
        # add to list of public videos

    pprint(response)
    print('hello')


def filter_video_ids_to_public_videos_only(youtube, video_ids):
    public_video_ids = []
    for video_id in video_ids:
        print(f'filter_video_ids_to_public_videos_only: video_id: {video_id}')
        request = youtube.videos().list(
            part="status,snippet,contentDetails,statistics",
            id=video_id
        )
        response = request.execute()
        privacy_status = response['items'][0]['status']['privacyStatus']
        if privacy_status == 'public':
            public_video_ids.append(video_id)
    return public_video_ids


def get_all_video_ids_for_my_channel(youtube) -> [str]:

    search = youtube.search()
    request = search.list(
        part="snippet",
        forMine=True,
        maxResults=25,
        type="video"
    )
    search_docs = []
    i = 0
    while request is not None:
        print(f'search_results_page {i}')
        i += 1
        search_doc = request.execute()
        search_docs.append(search_doc)
        request = search.list_next(request, search_doc)
    # print(search_docs)
    video_ids = []
    for search_doc in search_docs:
        for item in search_doc['items']:
            video_ids.append(item['id']['videoId'])

    return video_ids


    #activities = service.activities()
    #request = activities.list(userId='someUserId', collection='public')

    #while request is not None:
        #activities_doc = request.execute()

        # Do something with the activities

        # request = activities.list_next(request, activities_doc)



    # responses = []
    # request = youtube.search().list(
    #     part="snippet",
    #     forMine=True,
    #     maxResults=25,
    #     type="video"
    # )
    # response = request.execute()
    # responses.append(response)
    # while response.get('nextPageToken') is not None:
    #     request = youtube.search().list(
    #         part="snippet",
    #         forMine=True,
    #         maxResults=25,
    #         type="video",
    #         params=f'nextPageToken:{response.get("nextPageToken")}'
    #     )
    #     response = request.execute()
    #     responses.append(response)

    # print('hello')
    #
    # video_ids = []
    # for item in response['items']:
    #     video_ids.append(item["id"]["videoId"])
    # return video_ids
    # pprint(response)

def get_youtube():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    read_pickle = True
    write_pickle = False
    assert not (read_pickle and write_pickle)
    if read_pickle:
        with open('credentials.pickle', 'rb') as f:
            credentials = pickle.load(f)
    else:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
    if write_pickle:
        with open('credentials.pickle', 'wb') as f:
            pickle.dump(credentials, f)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    return youtube




if __name__ == "__main__":
    main()

