from __future__ import print_function
from twitchstream.outputvideo import TwitchOutputStreamRepeater
from twitchstream.chat import TwitchChatStream
import argparse
import time
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    required = parser.add_argument_group('required arguments')
    required.add_argument('-u', '--username',
                          help='twitch username',
                          required=True)
    required.add_argument('-o', '--oauth',
                          help='twitch oauth '
                               '(visit https://twitchapps.com/tmi/ '
                               'to create one for your account)',
                          required=False)
    args = parser.parse_args()

    if not args.oauth:
        f = open("oauth.properties", "r")
        auth = f.read()

    # Launch a verbose (!) twitch stream
    with TwitchChatStream(username=args.username,
                          oauth=auth,
                          verbose=True) as chatstream:

        chatstream.join_channel('existentiallyyours')
        # Send a message to this twitch stream
        for x in range(10):
            chatstream.send_chat_message("Oh Hello -"+ str(x) + "\r\n")

        # Continuously check if messages are received (every ~10s)
        # This is necessary, if not, the chat stream will close itself
        # after a couple of minutes (due to ping messages from twitch)
        while True:
            received = chatstream.twitch_receive_messages()
            if received:
                print("received:", received)
            time.sleep(1)
