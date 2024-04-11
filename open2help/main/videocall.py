"""
Jitsi API for instant videocall
"""

# URL parsing
import urllib.parse

def create_instant_call(room_name):
    domain = 'meet.jit.si'

    unique_name = urllib.parse.quote(room_name)

    # construct url
    url = f'https://{domain}/{unique_name}'

    # test
    print(url)

    return url

if __name__ == "__main__":
    create_instant_call("test-open2help")