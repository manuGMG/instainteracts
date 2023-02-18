# Common URLs
HOME = 'https://www.instagram.com/'
HASHTAG = f'{HOME}explore/tags/'

# Hashtag indexes
FIRST_HASHTAG_A = 0
FIRST_RECENT_HASHTAG_A = 9

# XPath selectors
HASHTAG_POSTS = '//a[div[div[img]]]'
LIKE_BUTTON = '//button[div[*[local-name()=\'svg\'][@aria-label=\'Like\']]]'
COMMENT_BUTTON = '//button[div[*[local-name()=\'svg\'][@aria-label=\'Comment\']]]'
COMMENT_TEXTAREA = '//textarea'
POST_BUTTON = '//div[text()=\'Post\']'
FOLLOW_BUTTONS = '//div[text()=\'Follow\']'
UNFOLLOW_BUTTONS = '//button/div/div[text()=\'Following\']'
UNFOLLOW_CONFIRMATION = '//*[text()=\'Unfollow\']'

# Timeouts/delays
TIMEOUT = 30
LOOP_DELAY = TIMEOUT / 2
TEXTAREA_TIMEOUT = TIMEOUT / 5
FOLLOW_DELAY = TIMEOUT / 5
UNFOLLOW_DELAY = TIMEOUT / 5
COMMENT_DELAY = TIMEOUT / 5
SHORT_DELAY = 1

# Window size
WIDTH = 375
HEIGHT = 1000

# Limits
MAX_FOLLOWS_PER_POST = 5
