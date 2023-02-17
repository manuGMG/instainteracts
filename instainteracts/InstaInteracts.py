import random
import time
from .helpers.const import *
from .helpers.options import options
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

class InstaInteracts:
    '''Wrapper Class

    Wraps all browser functions. When instantiated, creates a new
    Chrome driver, navigates to Instagram and attempts to log in.
    '''
    def __init__(self, username: str, password: str) -> None:
        # Get HOME URL
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

        # Set window size
        self.driver.set_window_size(WIDTH, HEIGHT)

        self.driver.get(HOME + '?1') # add ? to detect url change later

        # Input: username and password
        fields = WebDriverWait(self.driver, timeout=TIMEOUT) \
            .until(lambda d: d.find_elements(By.TAG_NAME, 'input'))
        fields[0].send_keys(username)
        fields[1].send_keys(password)

        # Login
        fields[1].send_keys(Keys.ENTER)

        # Wait until URL changes, as that means we are probably logged in
        WebDriverWait(self.driver, timeout=10) \
            .until(lambda d: d.current_url != HOME + '?1')
        
        self.driver.get(HOME)

    def _loop_posts_by_hashtag(self, hashtag: str, func: callable, only_recent: bool):
        '''_loop_posts_by_hashtag calls func() on every post of a given hashtag

        Args:
            hashtag (str): hashtag
            func (callable): function to be called after opening each post
            only_recent (bool): if True, only recent posts will be looped
        '''
        start = FIRST_RECENT_HASHTAG_A if only_recent else FIRST_HASHTAG_A

        # Get HASHTAG URL
        self.driver.get(HASHTAG + hashtag)
        
        # Get posts
        posts = WebDriverWait(self.driver, timeout=TIMEOUT) \
            .until(lambda d: d.find_elements(By.TAG_NAME, 'a'))[start:]
        
        urls = []
        for post in posts:
            urls.append(post.get_attribute('href'))

        for url in urls:
            self.driver.get(url)
            func()

    def follow_by_hashtag(self, hashtag: str, only_recent: bool = False):
        '''follow_by_hashtag follows users that have either posted using a hashtag or 
        liked posts using the hashtag

        Args:
            hashtag (str): hashtag
            only_recent (bool, optional): if True, only recent posts will be looped. Defaults to False.
        '''
        def follow():
            # Get users who liked the post
            self.driver.get(self.driver.current_url + 'liked_by/')

            # Get all follow buttons
            follow_btns = WebDriverWait(self.driver, timeout=TIMEOUT) \
                .until(lambda d: d.find_elements(By.XPATH, f'//div[text()=\'{FOLLOW_TEXT}\']'))

            for btn in follow_btns[:MAX_FOLLOWS_PER_POST]:
                self.driver.execute_script('arguments[0].scrollIntoView();', btn)
                btn.click()
                time.sleep(DELAY)
            
            self.driver.back()

        self._loop_posts_by_hashtag(hashtag, follow, only_recent)

    def like_by_hashtag(self, hashtag: str, only_recent: bool = False):
        '''like_by_hashtag likes posts with a given hashtag

        Args:
            hashtag (str): hashtag
            only_recent (bool, optional): if True, only recent posts will be looped. Defaults to False.
        '''
        def like():
            # Find like button
            like_btn = WebDriverWait(self.driver, timeout=TIMEOUT) \
                .until(lambda d: d.find_elements(By.TAG_NAME, 'svg'))[LIKE_BUTTON_SVG]
            
            # scroll to button and click
            self.driver.execute_script('arguments[0].scrollIntoView();', like_btn)
            like_btn.click()

        self._loop_posts_by_hashtag(hashtag, like, only_recent)

    def comment_by_hashtag(self, hashtag: str, comments: list[str], only_recent: bool = False):
        '''comment_by_hashtag comments posts with a given hashtag. Comments are selected randomly.

        Args:
            hashtag (str): hashtag
            comments (list[str]): list of comments
            only_recent (bool, optional): if True, only recent posts will be looped. Defaults to False.
        '''
        def comment():
            time.sleep(DELAY)

            # Attempt to click on the comment button
            try:
                WebDriverWait(self.driver, timeout=TIMEOUT) \
                .until(lambda d: d.find_elements(By.TAG_NAME, 'svg'))[COMMENT_BUTTON_SVG] \
                .click()
            except ElementNotInteractableException:
                WebDriverWait(self.driver, timeout=TIMEOUT) \
                .until(lambda d: d.find_elements(By.TAG_NAME, 'svg'))[COMMENT_BUTTON_SVG_FALLBACK] \
                .click()
            
            # Attempt to find the textarea
            # catch timeout -- as coments CAN be disabled for that post
            textarea = None
            try:
                textarea = WebDriverWait(self.driver, timeout=TEXTAREA_TIMEOUT) \
                    .until(lambda d: d.find_elements(By.TAG_NAME, 'textarea'))
            except TimeoutException:
                return

            # Scroll to textarea
            self.driver.execute_script('arguments[0].scrollIntoView();', textarea[COMMENT_TEXTAREA])
            time.sleep(DELAY)

            # Send comment
            textarea[COMMENT_TEXTAREA].click()
            actions = ActionChains(self.driver)
            actions.send_keys(comments[random.randint(0, len(comments) - 1)])
            actions.send_keys(Keys.ENTER)
            actions.perform()
            
            time.sleep(DELAY)

        self._loop_posts_by_hashtag(hashtag, comment, only_recent)
