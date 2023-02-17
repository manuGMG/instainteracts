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
    insta.comment_by_hashtag('futbol')