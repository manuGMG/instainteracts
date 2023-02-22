import os
import pytest
from instainteracts import InstaInteracts

'''
In order to run the following tests
you should first set I_USERNAME,
I_PASSWORD and I_DIRECTORY variables
'''

@pytest.fixture
def username():
    return os.environ.get('I_USERNAME')

@pytest.fixture
def password():
    return os.environ.get('I_PASSWORD')

@pytest.fixture
def directory():
    return os.environ.get('I_DIRECTORY')

def test_user_dir(username, password, directory):
    assert username and password and directory
    # Create a first instance
    InstaInteracts(username, password, user_data_dir=directory)

    # Open a second instance without passing username and password
    # to check if login session persisted
    InstaInteracts(None, None, user_data_dir=directory) # will timeout otherwise
