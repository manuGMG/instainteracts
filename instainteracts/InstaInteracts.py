import pyperclip
import random
import time
from .helpers.const import *
from .helpers.options import options
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

class InstaInteracts:
    '''Wrapper Class

    Wraps all driver functions. When instantiated, creates a new
    Chrome driver, navigates to Instagram and attempts to log in.

    Args:
        username (str): username
        password (str): password
        headless (bool, optional): if True, Chrome will run in headless mode. Defaults to False.
    '''
    def __init__(self, username: str, password: str, headless: bool = False) -> None:
        self.follows = 0
        self.username = username

        # Handle headless mode
        if headless:
            options.add_argument('--headless')

        # Get HOME URL
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

        # Set window size
        self.driver.set_window_size(WIDTH, HEIGHT)

        self.driver.get(HOME + '?1') # add ? to detect url change later

        # Input: username and password
        fields = WebDriverWait(self.driver, timeout=TIMEOUT) \
            .until(lambda d: d.find_elements(By.TAG_NAME, 'input'))
        fields[0].send_keys(self.username)
        fields[1].send_keys(password)

        # Login
        fields[1].send_keys(Keys.ENTER)

        # Wait until URL changes, as that means we are probably logged in
        WebDriverWait(self.driver, timeout=10) \
            .until(lambda d: d.current_url != HOME + '?1')
        
        self.driver.get(HOME)

    def _loop_posts_by_hashtag(self, hashtag: str, func: callable, only_recent: bool, limit: int = -1, follow_limit: int = -1) -> None:
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
            .until(lambda d: d.find_elements(By.XPATH, HASHTAG_POSTS))[start:]
        
        urls = []
        for post in posts:
            urls.append(post.get_attribute('href'))

        if limit == -1:
            limit = len(urls)

        for url in urls[:limit]:
            self.driver.get(url)
            func()

            if follow_limit != -1 and self.follows == follow_limit:
                self.follows = 0
                break

            time.sleep(LOOP_DELAY)

    def follow_by_hashtag(self, hashtag: str, limit: int, only_recent: bool = False) -> None:
        '''follow_by_hashtag follows users that have either posted using a hashtag or 
        liked posts using the hashtag

        Args:
            hashtag (str): hashtag
            limit (int): limit of follows
            only_recent (bool, optional): if True, only recent posts will be looped. Defaults to False.
        '''
        def follow():
            # Get users who liked the post
            self.driver.get(self.driver.current_url + 'liked_by/')

            # Get all follow buttons
            try:
                follow_btns = WebDriverWait(self.driver, timeout=TIMEOUT) \
                    .until(lambda d: d.find_elements(By.XPATH, FOLLOW_BUTTONS))
            except TimeoutException:
                # that post probably has no likes
                return

            for btn in follow_btns[:MAX_FOLLOWS_PER_POST]:
                self.driver.execute_script('arguments[0].scrollIntoView();', btn)
                btn.click()
                time.sleep(FOLLOW_DELAY)

                self.follows += 1
                if self.follows == limit:
                    break
            
            self.driver.back()

        self._loop_posts_by_hashtag(hashtag, follow, only_recent, follow_limit=limit)

    def like_by_hashtag(self, hashtag: str, limit: int, only_recent: bool = False) -> None:
        '''like_by_hashtag likes posts with a given hashtag

        Args:
            hashtag (str): hashtag
            limit (int): limit of likes
            only_recent (bool, optional): if True, only recent posts will be looped. Defaults to False.
        '''
        def like():
            try:
                # Find like button and click
                WebDriverWait(self.driver, timeout=TIMEOUT) \
                    .until(lambda d: d.find_element(By.XPATH, LIKE_BUTTON)).click()
            except ElementNotInteractableException:
                return

        self._loop_posts_by_hashtag(hashtag, like, only_recent, limit)

    def comment_by_hashtag(self, hashtag: str, comments: list[str], limit: int, only_recent: bool = False) -> None:
        '''comment_by_hashtag comments posts with a given hashtag. Comments are selected randomly.

        Args:
            hashtag (str): hashtag
            comments (list[str]): list of comments
            limit (int): limit of comments
            only_recent (bool, optional): if True, only recent posts will be looped. Defaults to False.
        '''
        def comment():
            # Attempt to find the textarea and publish button
            # catch timeout -- as comments CAN be disabled for that post
            textarea = None
            try:
                # Click comment button
                WebDriverWait(self.driver, timeout=TEXTAREA_TIMEOUT) \
                    .until(lambda d: d.find_element(By.XPATH, COMMENT_BUTTON)).click()

                textarea = WebDriverWait(self.driver, timeout=TEXTAREA_TIMEOUT) \
                    .until(lambda d: d.find_elements(By.XPATH, COMMENT_TEXTAREA))[0]
            except TimeoutException:
                return
            
            self.driver.execute_script('arguments[0].scrollIntoView();', textarea)
            textarea.click()
            time.sleep(SHORT_DELAY)

            # Send comment
            actions = ActionChains(self.driver)
            pyperclip.copy(random.choice(comments))
            actions.key_down(Keys.CONTROL).send_keys('V').key_up(Keys.CONTROL)
            actions.send_keys(Keys.ENTER)
            actions.perform()
            
            time.sleep(COMMENT_DELAY)
            self.driver.back()

        self._loop_posts_by_hashtag(hashtag, comment, only_recent, limit)

    def unfollow(self, limit: int) -> None:
        '''unfollow unfollows {limit} users

        Args:
            limit (int): limit of users to unfollow
        '''
        unfollows = 0

        self.driver.get(f'{HOME}{self.username}/following')

        unfollow_btns = WebDriverWait(self.driver, timeout=TIMEOUT) \
            .until(lambda d: d.find_elements(By.XPATH, UNFOLLOW_BUTTONS))

        for btn in unfollow_btns[1:]:
            self.driver.execute_script('arguments[0].scrollIntoView();', btn)
            btn.click()

            # Confirm unfollow
            WebDriverWait(self.driver, timeout=TIMEOUT) \
            .until(lambda d: d.find_element(By.XPATH, UNFOLLOW_CONFIRMATION)).click()

            time.sleep(UNFOLLOW_DELAY)

            unfollows += 1
            if unfollows == limit:
                break
