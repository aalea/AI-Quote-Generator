# Bot that generates Danny Phantom lines based on the show's transcript
# Gets smarter with each run (runs a pass-through with each run

from textgenrnn import textgenrnn

import oauth2
from urllib import parse
import pytumblr

import sys
import io

CHARACTER = 'Danny Fenton'

REQUEST_TOKEN_URL = 'http://www.tumblr.com/oauth/request_token'
AUTHORIZATION_URL = 'http://www.tumblr.com/oauth/authorize'
ACCESS_TOKEN_URL = 'http://www.tumblr.com/oauth/access_token'

CONSUMER_KEY = 'x'
CONSUMER_SECRET = 'x'
OAUTH_TOKEN = 'x'
OAUTH_SECRET = 'x'

BLOG_NAME = 'dannyphantombot'
TAGS = ['danny phantom', 'AI-generated quote', 'machine learning', 'danny fenton']

def setup_model():
    textgen = textgenrnn(CHARACTER + '_weights.hdf5')
    textgen.train_from_file(CHARACTER + '.txt', num_epochs=1)
    return textgen

def generate_quote(textgen):
    generated_quote = 'did not work'

    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    textgen.generate(temperature=0.3)

    generated_quote = new_stdout.getvalue()
    sys.stdout = old_stdout

    print(generated_quote.split('\n')[0])
    return generated_quote.split('\n')[0]


def post_quote(generated_quote):

    client = pytumblr.TumblrRestClient(
        CONSUMER_KEY,
        CONSUMER_SECRET,
        OAUTH_TOKEN,
        OAUTH_SECRET,
    )

    # Creating a text post
    client.create_text(BLOG_NAME, state="queue", body=generated_quote, tags=TAGS)


def setup():
    textgen = setup_model()

    for x in range(30):
        generated_quote = generate_quote(textgen)
        post_quote(generated_quote)

    print('Posts successfully queued')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    setup()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
