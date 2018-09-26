from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import random

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

try:
    accept_button = driver.find_element_by_link_text('Got it!')
    accept_button.click()
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
        upgrades_enabled = driver.find_elements_by_xpath('//*[@class="upgrade unlocked enabled"]')
        if upgrades_enabled:
            for upgrade in reversed(upgrades_enabled):
                upgrade.click()


counter = 0
ticker = 0
while True:
    try:
        cookie_clicker()
        counter += 1
        if counter >= random.randrange(1000,2000):
            counter = 0
            ticker += 1
            product_checker()
            if ticker >= random.randrange(10,20):
                ticker = 0
                upgrades_checker()
    except Exception as e:
        print(e)
