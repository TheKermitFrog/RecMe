from spotipy import Spotify
import spotipy.util
import json
import os

def set_dir():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

def view_credentials():
    if not os.path.exists('credentials.txt'):
        print('No saved credentials found, input set_credentials to set credentials.')
    else:
        with open('credentials.txt', "r") as read:
            credentials = json.load(read)
            print('Username: {}'.format(credentials['username']))
            print('Client Id: {}'.format(credentials['client_id']))
            print('Client_Secret: {}'.format(credentials['client_secret']))
            print('Redirect URI: {}'.format(credentials['redirect_uri']))

def set_credentials():
    username = input('Spotify username:')
    client_id = input('Spotify Client Id:')
    client_secret = input('Spotify Client Secret:')
    redirect_uri = input('Your redirect URI:')
    credentials = {
        'username': username,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri
    }
    with open('credentials.txt', 'w') as outfile:
        json.dump(credentials, outfile)
    print('Credentials Saved')
    return username, client_id, client_secret, redirect_uri

def loggin():
    if not os.path.exists('credentials.txt'):
        print('Welcome to RecMe!\nLooks like it\'s your first time here, please enter your information.\n')
        username, client_id, client_secret, redirect_uri = set_credentials()
        print('Loggin you in....')
        print('Successfully logged in')
        token = spotipy.util.prompt_for_user_token(username,
                                           'playlist-modify-public user-read-private playlist-modify-private user-top-read user-read-recently-played user-follow-read',
                                           client_id,
                                           client_secret,
                                           redirect_uri)
        spotify = spotipy.Spotify(auth=token)
        print('{}, welcome to RecMe!'.format(spotify.me().get('display_name')))
        return spotify
    else:
        with open('credentials.txt', "r") as read:
                credentials = json.load(read)
                username = credentials['username']
                client_id = credentials['client_id']
                client_secret = credentials['client_secret']
                redirect_uri = credentials['redirect_uri']
        print('Loggin you in....')
        token = spotipy.util.prompt_for_user_token(username,
                                           'playlist-modify-public user-read-private playlist-modify-private user-top-read user-read-recently-played user-follow-read',
                                           client_id,
                                           client_secret,
                                           redirect_uri)
        spotify = spotipy.Spotify(auth=token)
        print('Successfully logged in')
        print('Welcome back {}!'.format(spotify.me().get('display_name')))
        return spotify

class RecMe():
    def __init__(self, spotify):
        self.spotify = spotify
        self.id = spotify.me().get('id')
        self.genres = spotify.recommendation_genre_seeds().get('genres')
        self.playlists = parse_playlists(spotify.current_user_playlists())
        self.destination = {}
        self.top_artists = parse_artists(spotify.current_user_top_artists())
        self.top_tracks = parse_tracks(spotify.current_user_top_tracks())

    def get_genres(self):
        print(self.genres)
    def get_playlists(self):
        print(self.playlists)
    def set_destination(self):
        dest = input('Enter destination playlist id:')
        temp = self.spotify.playlist(playlist_id=dest)
        if temp.get('owner').get('id') != self.id:
            print('You do not own this playlist. Please use a playlist you owned.')
        else:
            self.destination['id'] = dest
            self.destination['name'] = temp.get('name')
            print('Destination set to: {}'.format(temp.get('name')))
    def current_destination(self):
        if self.destination:
            print('Your destination is set to: {}'.format(self.destination.get('name')))
        else:
            print('No destination set, RecMe will create a new playlist as destination.')
    def getrec(self):
        print('Input must be separated by comma')
        while True:
            try:
                seed_artists = input('Enter seed artist ids:')
                seed_tracks = input('Enter seed track ids:')
                seed_genres = input('Enter seed genres:')
                seed_artists, seed_tracks, seed_genres = seeds_handler(seed_artists), seeds_handler(seed_tracks), seeds_handler(seed_genres)

                seeds_num = len(seed_artists) + len(seed_tracks) + len(seed_genres)
                if seeds_num > 5 or seeds_num == 0:
                    raise SeedsNumberException()
                break
            except SeedsNumberException:
                print('Maximum is five seeds. At least one of seed_artists, seed_tracks and seed_genres are needed.')

        while True:
            try:
                limit = int(input('How many tracks to recommend (1-100):'))
                if limit >= 1 and limit <= 100:
                    break
            except ValueError:
                print('Please enter an integer between 1 and 100')

        # get recommendation
        rec_tracks = self.spotify.recommendations(seed_artists=seed_artists, seed_genres=seed_genres, seed_tracks=seed_tracks, limit=limit)
        track_ids = parse_rec(rec_tracks)
        # todo
        # inplement rec playlist
        if rec_tracks:
            if not self.destination:
                description = 'Custom recommendations from RecMe'
                playlist = self.spotify.user_playlist_create(user=self.id, name='RecMe Recommendations', description=description)
                dest = playlist.get('id')
                self.spotify.user_playlist_add_tracks(user=self.id, playlist_id=dest, tracks=track_ids)
                print('Done')
            else:
                self.spotify.user_playlist_add_tracks(user=self.id, playlist_id=self.destination, tracks=track_ids)
                print('Done')

# helper functions
def parse_playlists(playlists):
    parsed = {}
    for playlist in playlists.get('items'):
        parsed[playlist.get('name')] = playlist.get('id')
    return parsed

def parse_artists(artists):
    parsed = {}
    for artist in artists.get('items'):
        parsed[artist.get('name')] = artist.get('id')
    return parsed

def parse_tracks(tracks):
    parsed = {}
    for track in tracks.get('items'):
        parsed[track.get('name')+'-'+track.get('artists')[0].get('name')] = track.get('id')
    return parsed

def seeds_handler(seeds):
    if seeds:
        return seeds.split(',')
    else:
        return seeds

def parse_rec(recs):
    tracks_id = []
    for rec in recs.get('tracks'):
        tracks_id.append(rec.get('id'))
    return(tracks_id)

class SeedsNumberException(BaseException):
    pass

help = """Commands
Login not required:
-login: Login to with saved credentials.
        Credentials:
        * Spotify username: Spotify user URI
        * Spotyfy client ID = Spotify developer account client ID
        * Spotify client secret = Spotify developer account client secret
        * Redirect URI = Spotify developer account redirect URI
-view_credentials: View saved credentials.
-set_credentials: Update credentials.

Login required:
-get_genres: Return a list of available seed genres.
-get_playlists: Return a list of your Spotify playlists and their ids.
-set_destination: Set destination playlist for recommendations.
-current_destination: Display current destination.
-my_top_artists: Return a list of your top artists and their ids.
-my_top_tracks: Return a list of your top tracks and their ids.
-getrec: Get recommendations, add them to your destination playlist.
         If no destination playlist is set, RecMe creates a new playlist "RecMe Recommendations" as destination.
         4 arguments needed:
         * seed artist: Seed artists ids, separated by comma.
         * seed track: Seed tracks ids, separated by comma.
         * seed genres: Seed genres, separated by comma.
         Maximum is five seeds in total. At least one of seed_artists, seed_tracks and seed_genres are needed.
         * Number of tracks to recommend: Integer with value between 1 and 100.

"""

def main():
    set_dir()
    while True:
        cmd = input('')
    # matches = [f for f in os.listdir() if f.startswith(".cache-")]
        if cmd == 'login':
            spotify = loggin()
            recme = RecMe(spotify)
        elif cmd == 'view_credentials':
            view_credentials()
        elif cmd == 'set_credentials':
            set_credentials()
        elif cmd == 'get_genres':
            try:
                recme.get_genres()
            except UnboundLocalError:
                print('You havn\'t logged in, type login to login.')
        elif cmd == 'get_playlists':
            try:
                recme.get_playlists()
            except UnboundLocalError:
                print('You havn\'t logged in, type login to login.')
        elif cmd == 'set_destination':
            try:
                recme.set_destination()
            except UnboundLocalError:
                print('You havn\'t logged in, type login to login.')
        elif cmd == 'current_destination':
            try:
                recme.current_destination()
            except UnboundLocalError:
                print('You havn\'t logged in, type login to login.')
        elif cmd == 'my_top_artists':
            try:
                print(recme.top_artists)
            except UnboundLocalError:
                print('You havn\'t logged in, type login to login.')
        elif cmd == 'my_top_tracks':
            try:
                print(recme.top_tracks)
            except UnboundLocalError:
                print('You havn\'t logged in, type login to login.')
        elif cmd == 'getrec':
            try:
                recme.getrec()
            except UnboundLocalError:
                print('You havn\'t logged in, type login to login.')
        elif cmd == 'help':
            print(help)
        else:
            print('Unknown command {}, type help for available commands.'.format(cmd))

if __name__ == '__main__':
    main()
