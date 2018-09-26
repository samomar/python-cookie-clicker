from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import random
import time

chrome_path = "your_chrome_path_here"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir=cookie-clicker")
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chrome_path, options=chrome_options)

driver.get('http://orteil.dashnet.org/cookieclicker/')

big_cookie = driver.find_element_by_id('bigCookie')
golden_cookie = driver.find_element_by_id('goldenCookie')
seasonPopup = driver.find_element_by_id('seasonPopup')

def accept_cookie():
    accept_button = accept_button = driver.find_element_by_link_text('Got it!')
    accept_button.click()

try:
    accept_cookie()
except:
    try:
        time.sleep(2)
        accept_cookie()
    except:
        pass

def cookie_clicker():
    ActionChains(driver).double_click(big_cookie).perform()

def product_checker():
    first_product = driver.find_element_by_css_selector('#product0').get_attribute('class')
    if first_product == 'product unlocked enabled':
        products_enabled = driver.find_elements_by_xpath('//*[@class="product unlocked enabled"]')
        if products_enabled:
            for product in reversed(products_enabled):
                product.click()

def upgrades_checker():
    first_upgrade = driver.find_element_by_css_selector('#upgrade0').get_attribute('class')
    if first_upgrade == 'crate upgrade enabled':
        upgrades_enabled = driver.find_elements_by_xpath('//*[@class="crate upgrade enabled"]')
        if upgrades_enabled:
            for upgrade in upgrades_enabled:
                upgrade.click()


counter = 0
ticker = 0
while True:
    try:
        cookies = driver.find_element_by_id('cookies').text.split(' ')[0]
        cookie_clicker()
        counter += 1
        if counter >= random.randrange(1000,10000):
            counter = 0
            ticker += 1
            product_checker()
            if ticker >= random.randrange(10,20):
                ticker = 0
                upgrades_checker()
    except Exception as e:
