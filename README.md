# RecMe
A enhanced Spotify tracks recommendation tool.

## How does it works
1. Logs on to your Spotify account.
2. Recommends tracks based on provided seed artists, tracks, and genres.
3. Adds them to your playlist of choice.

## Before you use it:
* Login to Spotify Developer Dashboard and create a new app to obtain the Client ID and Client Secret. Add these to CLIENT_ID and CLIENT_SECRET in the code. After this, click edit settings of the newly created app and add an URI to Redirect URIs and save, if you don't have a URI in mind, just use https://www.google.com/.

* Spotipy : Spotipy is a lightweight Python library for the Spotify Web API. With Spotipy you get full access to all of the music data provided by the Spotify platform, run```pip install requirements.txt```.  

## If you want to use it
1. Clone repository.
2. run python3 RecMe.py

### First time run

#### Authorize application
While your first run you are asked to authorize RecMe in your Spotify account so it can access and modify your playlists, and read your top artists and tracks.

The prompt will look like this:

```
            User authentication requires interaction with your
            web browser. Once you enter your credentials and
            give authorization, you will be redirected to
            a url.  Paste that url you were directed to to
            complete the authorization.


Opened https://accounts.spotify.com/authorize?redirect_uri=<your_redirect_uri>&response_type=code&client_id=<client_id>&scope=user-follow-read in your browser


Enter the URL you were redirected to:

```

Open the link in your browser, authorize the application and you will be redirected to the redirect URI. Copy the URL and paste it into the terminal. This will generate the `.cache_<your_user_name>` file in the project folder. The next time you run the script everything works out as you'd wish for.
