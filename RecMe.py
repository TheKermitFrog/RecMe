from spotipy import Spotify
import spotipy.util
import json
import argparse
import os.path
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
        self.destination = ''

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
            self.destination = dest
            print('Destination set to: {}'.format(temp.get('name')))



def parse_playlists(playlists):
    parsed = {}
    for playlist in playlists.get('items'):
        parsed[playlist.get('name')] = playlist.get('id')
    return parsed
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
        else:
            print('Unknown command {}, type help for available commands.'.format(cmd))



    # args = get_args()
    # if args.file_path:
    #     with open(args.file_path) as file:
    #         file.write('Lorem ipsum dolor sit.')


if __name__ == '__main__':
    main()
