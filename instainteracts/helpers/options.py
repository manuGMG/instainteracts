from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('lang=en-GB')
options.add_argument('--disable-blink-features=AutomationControlled')
