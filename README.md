# My YouTube Analytics Repository

Usage

- Python 3.11 recommended
- Clone this repository.
- Set up a virtual environment and install dependencies with `pip install -r requirements.txt`
- Put YouTube API credentials in a file named client_secret.json in the root directory
- This YouTube API credentials file should allow read access to both the YouTube Data API v3 and the YouTube Analytics API
- For the first local run, you will need to set `write_pickle=True` and `read_pickle=False` in the functions `get_youtube` and `get_youtube_for_analytics` in the file `valid_public_watch_hours.py`. That take you through the auth flow and will save a credentials object in `credentials.pickle`. Take care not to share this pickle file, as it grants access to the YouTube API.
- For subsequent runs you may set `read_pickle=True` and `write_pickle=False` to read the credentials object from the local pickle file, which will save you the trouble of authenticating through your browser on every run.
- At the start of the `main` function in `valied_public_watwch_hours.py`, set the variables `start_date` and `end_date` to your desired time window, using string of format `'%Y-%m-%d'`.
- Create a directory named `output` in the root directory of this project.
- Execute `python valid_public_watch_hours.py` in the root directory of this project.
- The script will print information to your console while running, and also save a file in the output directory with summary information about the run.

Caveats:


