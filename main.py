from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

URL = "https://orteil.dashnet.org/cookieclicker/"
# Modify this line to reflect the path needed for your chromedriver.exe
# the chromedriver.exe version must match the Chrome browser version
chrome_driver_path = r"C:\Users\jrpgt\Documents\Development\chromedriver.exe"

ser = Service(chrome_driver_path)
driver = webdriver.Chrome(options=chrome_options, service=ser)
# Not sure how this work, but it was part of my solution to clicking through the language selector
action = ActionChains(driver)
driver.get(URL)

#
# 1. get cookie to click
# 2. Setup timer for exit game
# 3. Get list of product elements, total 19 products, 0 - 18 "id=product{n}"
# 4. Get list of upgrades, total 8? "id=upgrade{n}"
# 5. Check list of upgrades and products every 5 seconds, click products to buy until no cookies

# The website is dynamic, so give it a few seconds to load
time.sleep(5)


# Use the action object to navigate to the language select popup and click it
navigate = driver.find_element(By.ID, "langSelect-EN")
action.move_to_element(navigate).perform()
# driver.execute_script("arguments[0].click();", navigate)
navigate.click()

# Give website a few more seconds to load after language selection, before clicking cookies
time.sleep(5)

# Set up cookies and timer variables
cookie = driver.find_element(By.ID, "bigCookie")
start_time = time.time()
seconds = 60 * 60 * 5  # Duration of program
time_check = 15  # How often to check for upgrades and products
timeout = time.time() + time_check
golden_cookie_count = 0

purchase_wait_1 = 60 * 5        # After 5 minutes
purchase_wait_2 = 60 * 10       # After 10 minutes
purchase_wait_3 = 60 * 20       # After 20 minutes


while True:
    current_time = time.time()
    elapsed_time = current_time - start_time
    # driver.execute_script("arguments[0].click();", cookie)
    cookie.click()

    # Click the golden cookie
    try:
        golden_cookie = driver.find_element(By.CLASS_NAME, 'shimmer')
        golden_cookie.click()
        golden_cookie_count += 1
    except:
        pass

    if time.time() > timeout:
        # Check to purchase upgrades first
        for n in range(8, -1, -1):
            try:
                upgrade = driver.find_element(By.ID, f"upgrade{n}")
                upgrade.click()
            except:
                pass
        # Check to purchase products second
        for n in range(19, -1, -1):
            try:
                product = driver.find_element(By.ID, f"product{n}")
                check_class = product.get_attribute("class")
                # buy as many of the highest tier product possible
                while check_class == "product unlocked enabled":
                    product.click()
                    check_class = product.get_attribute("class")
            except:
                pass

        timeout = time.time() + time_check

    if elapsed_time > purchase_wait_1:
        time_check = 30

    if elapsed_time > purchase_wait_2:
        time_check = 60

    if elapsed_time > purchase_wait_3:
        time_check = 120

    if elapsed_time > seconds:
        cookies_per_second = driver.find_element(By.ID, "cookiesPerSecond")
        cps = cookies_per_second.text
        print(f"Cookies baked {cps}")
        print(f"Golden cookies clicked: {golden_cookie_count}")
        print("finished")

        break
