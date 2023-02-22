from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('lang=en-GB')
options.add_argument('user-agent='
                     'Mozilla/5.0(Windows NT 10.0; Win64; x64)'
                     'AppleWebKit/537.36 (KHTML, like Gecko)'
                     'Chrome/108.0.0.0 Safari/537.36')
options.add_argument('--disable-blink-features=AutomationControlled')
