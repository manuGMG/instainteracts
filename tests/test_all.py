import os
import pytest
from instainteracts import InstaInteracts

@pytest.fixture
def username():
    return os.environ.get('I_USERNAME')

@pytest.fixture
def password():
    return os.environ.get('I_PASSWORD')

def test_hashtag(username, password):
    assert username and password
    insta = InstaInteracts(username, password)
    
    insta.comment_by_hashtag('instagram', [
        u'🔥🔥'
    ], only_recent=True, limit=2)

    insta.follow_by_hashtag('instagram', limit=2)

    insta.like_by_hashtag('instagram', limit=2)
