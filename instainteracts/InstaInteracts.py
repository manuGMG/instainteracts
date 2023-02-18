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
        self.follows = 0
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

    def _loop_posts_by_hashtag(self, hashtag: str, func: callable, only_recent: bool, limit: int = -1, follow_limit: int = -1):
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

        if limit == -1:
            limit = len(urls)

        for url in urls[:limit]:
            self.driver.get(url)
            func()

            if follow_limit != -1 and self.follows == follow_limit:
                self.follows = 0
                break

            time.sleep(LOOP_TIMEOUT)

    def follow_by_hashtag(self, hashtag: str, only_recent: bool = False, limit: int = FOLLOW_LIMIT):
        '''follow_by_hashtag follows users that have either posted using a hashtag or 
        liked posts using the hashtag

        Args:
            hashtag (str): hashtag
            only_recent (bool, optional): if True, only recent posts will be looped. Defaults to False.
            limit (int, optional): limit of follows. Defaults to FOLLOW_LIMIT.
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

                self.follows += 1
                if self.follows == limit:
                    break
                
                time.sleep(DELAY)
            
            self.driver.back()

        self._loop_posts_by_hashtag(hashtag, follow, only_recent, follow_limit=limit)

    def like_by_hashtag(self, hashtag: str, only_recent: bool = False, limit: int = LIKE_LIMIT):
        '''like_by_hashtag likes posts with a given hashtag

        Args:
            hashtag (str): hashtag
            only_recent (bool, optional): if True, only recent posts will be looped. Defaults to False.
            limit (int, optional): limit of likes. Defaults to LIKE_LIMIT.
        '''
        def like():
            try:
                # Find like button
                like_btn = WebDriverWait(self.driver, timeout=TIMEOUT) \
                    .until(lambda d: d.find_elements(By.TAG_NAME, 'svg'))
                
                # scroll to button and click
                for index in LIKE_BUTTON_SVG:
                    self.driver.execute_script('arguments[0].scrollIntoView();', like_btn[index])
                    like_btn[index].click()
            except ElementNotInteractableException:
                return

        self._loop_posts_by_hashtag(hashtag, like, only_recent, limit)

    def comment_by_hashtag(self, hashtag: str, comments: list[str], only_recent: bool = False, limit: int = COMMENT_LIMIT):
        '''comment_by_hashtag comments posts with a given hashtag. Comments are selected randomly.

        Args:
            hashtag (str): hashtag
            comments (list[str]): list of comments
            only_recent (bool, optional): if True, only recent posts will be looped. Defaults to False.
            limit (int, optional): limit of comments. Defaults to COMMENT_LIMIT.
        '''
        def comment():
            time.sleep(DELAY)

            # Attempt to click on the comment button
            try:
                WebDriverWait(self.driver, timeout=TIMEOUT) \
                .until(lambda d: d.find_elements(By.TAG_NAME, 'svg'))[COMMENT_BUTTON_SVG[0]] \
                .click()
            except ElementNotInteractableException:
                WebDriverWait(self.driver, timeout=TIMEOUT) \
                .until(lambda d: d.find_elements(By.TAG_NAME, 'svg'))[COMMENT_BUTTON_SVG[1]] \
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

        self._loop_posts_by_hashtag(hashtag, comment, only_recent, limit)
