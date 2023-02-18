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
        'Nice'
    ], limit=1)
    insta.comment_by_hashtag('instagram', [
        'Great'
    ], limit=1, only_recent=True)

    insta.follow_by_hashtag('instagram', limit=1)
    insta.follow_by_hashtag('instagram', limit=1, only_recent=True)

    insta.like_by_hashtag('instagram', limit=1)
    insta.like_by_hashtag('instagram', limit=1, only_recent=True)

    insta.unfollow(2)
