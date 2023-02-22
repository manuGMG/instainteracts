# InstaInteracts
InstaInteracts is an automation tool for Instagram interactions (follow, like, comment).

## How to install
You can install instainteracts by running the following command:
```
pip install instainteracts
```

## Basic usage
The following example shows how to use InstaInteracts:
```py
from instainteracts import InstaInteracts

username = '' # your username
password = '' # your password
hashtag = 'insta' # hashtag to interact with

insta = InstaInteracts(username, password)
# for all optional arguments, read the docs below

insta.comment_by_hashtag(
    hashtag,
    ['Comment', u'Emojis supported 🔥'], # list of comments
    only_recent=True, # interact only with recent posts
    limit=1 # limit of comments
)

insta.follow_by_hashtag(
    hashtag,
    limit=2 # limit of follows
)

insta.like_by_hashtag(
    hashtag,
    limit=3 # limit of likes
)

insta.unfollow(5) # will unfollow 5 users
```

## Docs
All InstaInteracts methods are documented at https://instainteracts.pages.dev