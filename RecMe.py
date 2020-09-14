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

def loggin():
    if not os.path.exists('credentials.txt'):
        print('Welcome to RecMe!\nSince this is your first time here, please enter your information.\n')
        username = input('Spotify username:')
        client_id = input('Spotify Client Id:')
        client_secret = input('Spotify Client Secret:')
        redirect_uri = input('Your redirect uri:')
        credentials = {
            'username': username,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri
        }
        with open('credentials.txt', 'w') as outfile:
            json.dump(credentials, outfile)
        token = spotipy.util.prompt_for_user_token(username,
                                           'playlist-modify-public',
                                           client_id,
                                           client_secret,
                                           redirect_uri)
        sp = spotipy.Spotify(auth=token)
        print('Welcome {}!'.format(sp.me().get('display_name')))
        return sp
    else:
        with open('credentials.txt', "r") as out:
                credentials = json.load(out)
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
        print('Welcome {}!'.format(sp.me().get('display_name')))
        return sp




def main():
    set_dir()
    # matches = [f for f in os.listdir() if f.startswith(".cache-")]
    sp_client = loggin()


    # args = get_args()
    # if args.file_path:
    #     with open(args.file_path) as file:
    #         file.write('Lorem ipsum dolor sit.')


if __name__ == '__main__':
    main()
