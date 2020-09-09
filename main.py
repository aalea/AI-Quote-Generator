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

BLOG_NAME = 'dannyfentonaiquotes'
TAGS = ['danny phantom', 'AI-generated quote', 'machine learning', 'danny fenton']

def setup_model():
    #textgen = textgenrnn()
    #textgen.train_from_file(CHARACTER + '.txt', num_epochs=1) #increase epochs for more accurate quotes
    textgen = textgenrnn('textgenrnn_weights.hdf5')
    return textgen

def generate_quote(textgen):
    generated_quote = 'did not work'

    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout

    textgen.generate(temperature=0.2)

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

    for x in range(50): #tumblr allows up to 50 queued posts a day
        generated_quote = generate_quote(textgen)
        #print(generated_quote)
        #generated_quote = 'testing......'
        post_quote(generated_quote)

    print('Posts successfully queued')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    setup()
