from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import operator
import time

chrome_path = "your_chrome_path_here"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("user-data-dir=cookie-clicker")
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_path, options=chrome_options)

driver.get('http://orteil.dashnet.org/cookieclicker/')

big_cookie = driver.find_element_by_id('bigCookie')
golden_cookie = driver.find_element_by_id('goldenCookie')
seasonPopup = driver.find_element_by_id('seasonPopup')

products_dict = {}
upgrades_dict = {}

list_of_zero_nums = {
    'million': 6,
    'billion': 9,
    'trillion': 12,
    'quadrillion': 15,
    'quintillion': 18,
    'sextillion': 21,
    'septillion': 24,
    'octillion': 27,
    'nonillion': 30,
    'decillion': 33,
}


def number_cleaner(number):
    for key, value in list_of_zero_nums.items():
        if key in number:
            grab = list_of_zero_nums.get(key, 1)
            zeros = ''
            for i in range(grab):
                zeros += '0'
            result = int(number.replace(key, zeros).replace(' ', '').replace('.', '').replace(',', ''))
            return result
    return number


def current_cookies():
    cookies = number_cleaner(driver.find_element_by_id('cookies').text.split('cookies')[0])
    return int(cookies)


def accept_cookie():
    accept_button = driver.find_element_by_link_text('Got it!')
    accept_button.click()


try:
    accept_cookie()
except Exception as e:
    print(e)
    try:
        time.sleep(2)
        accept_cookie()
    except Exception as e:
        print(e)
        pass


def price_checker(entity):
    ActionChains(driver).move_to_element(entity).perform()
    price = driver.find_element_by_id('tooltip').find_element_by_class_name("price").text.replace(',', '')
    product_price = number_cleaner(price)
    product_name = driver.find_element_by_id('tooltip').find_element_by_class_name("name").text
    return product_price, product_name


def product_checker():
    first_product = driver.find_element_by_css_selector('#product0').get_attribute('class')
    if first_product == 'product unlocked enabled':
        products_enabled = driver.find_elements_by_xpath('//*[@class="product unlocked enabled"]')
        if products_enabled:
            for product in reversed(products_enabled):
                pass
                product_data = price_checker(product)
                price, name = product_data
                if name and price:
                    products_dict[name] = int(price)
                    if is_product_worthy(products_dict):
                        product.click()


def upgrades_checker():
    max_product_value = max(products_dict.items(), key=operator.itemgetter(1))[1]
    first_upgrade = driver.find_element_by_css_selector('#upgrade0').get_attribute('class')
    if first_upgrade == 'crate upgrade enabled':
        upgrades_enabled = driver.find_elements_by_xpath('//*[@class="crate upgrade enabled"]')
        if upgrades_enabled:
            for upgrade in upgrades_enabled:
                price, name = price_checker(upgrade)
                if price and name:
                    upgrades_dict[name] = price

                    if int(max_product_value) >= int(upgrades_dict[name] * 3):
                        upgrade.click()


def is_product_worthy(entity_dict):
    max_entity_value = max(entity_dict.items(), key=operator.itemgetter(1))[1]
    cookies = int(current_cookies())
    if (cookies / 100 * 50) < max_entity_value:
        return False
    else:
        return True


cookie_clicker = """
// Javascript is faster for clicking - credit: jeresig
    CookieClicker = {
        start: function () {
            this.clickInterval = setInterval(function () {
                document.getElementById("bigCookie").click();
            });

            this.goldInterval = setInterval(function () {
                var shimmer = document.getElementsByClassName("shimmer")[0];
                if (shimmer) {
                    shimmer.click();
                }
            }, 1000);
        }
    };

CookieClicker.start();
"""

try:
    driver.execute_script(cookie_clicker)
except Exception as e:
    print(e)
    try:
        time.sleep(2)
        driver.execute_script(cookie_clicker)
    except Exception as e:
        print(e)
        exit()

while True:
    try:
        product_checker()
        time.sleep(1)
        upgrades_checker()
        time.sleep(1)
    except Exception as e:
        print(e)
