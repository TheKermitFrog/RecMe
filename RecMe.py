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
        token = spotipy.util.prompt_for_user_token(username,
                                           'playlist-modify-public',
                                           client_id,
                                           client_secret,
                                           redirect_uri)
        sp = spotipy.Spotify(auth=token)
        print('Welcome {}!'.format(sp.me().get('display_name')))
        return sp
    else:
        with open('credentials.txt', "r") as read:
                credentials = json.load(read)
                username = credentials['username']
                client_id = credentials['client_id']
                client_secret = credentials['client_secret']
                redirect_uri = credentials['redirect_uri']
        token = spotipy.util.prompt_for_user_token(username,
                                           'playlist-modify-public',
                                           client_id,
                                           client_secret,
                                           redirect_uri)
        sp = spotipy.Spotify(auth=token)
        print('Welcome back {}!'.format(sp.me().get('display_name')))
        return sp





def main():
    set_dir()
    while True:
        cmd = input()
    # matches = [f for f in os.listdir() if f.startswith(".cache-")]
        if cmd == 'login':
            sp_client = loggin()
        elif cmd == 'view_credentials':
            view_credentials()
        elif cmd == 'set_credentials':
            set_credentials()



    # args = get_args()
    # if args.file_path:
    #     with open(args.file_path) as file:
    #         file.write('Lorem ipsum dolor sit.')


if __name__ == '__main__':
    main()
