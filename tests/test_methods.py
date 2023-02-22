import os
import pytest
from instainteracts import InstaInteracts

'''
In order to run the following tests
you should first set I_USERNAME and
I_PASSWORD variables
'''

@pytest.fixture
def insta():
    username = os.environ.get('I_USERNAME')
    password = os.environ.get('I_PASSWORD')
    if username and password: return InstaInteracts(username, password)

def test_methods(insta):
    assert insta
    insta.comment_by_hashtag('instagram', [u'🔥🔥'], limit=1)
    insta.comment_by_hashtag('instagram', [u'🔥'], limit=1, only_recent=True)

    insta.follow_by_hashtag('instagram', limit=1)
    insta.follow_by_hashtag('instagram', limit=1, only_recent=True)

    insta.like_by_hashtag('instagram', limit=1)
    insta.like_by_hashtag('instagram', limit=1, only_recent=True)

    insta.unfollow(2)
