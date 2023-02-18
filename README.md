# InstaInteracts
InstaInteracts is an automation tool for Instagram interactions (follow, like, comment).

## Basic usage
```py
from instainteracts import InstaInteracts

username = '' # your username
password = '' # your password
hashtag = 'insta' # hashtag to interact with

insta = InstaInteracts(username, password)

insta.comment_by_hashtag(
    hashtag,
    ['nice', 'hi'], # List of comments
    only_recent=True, # Interact only with recent posts
    limit=10 # limit of comments
)

insta.follow_by_hashtag(
    hashtag,
    limit=2 # limit of follows
)

insta.like_by_hashtag(
    hashtag,
    limit=5 # limit of likes
)
```