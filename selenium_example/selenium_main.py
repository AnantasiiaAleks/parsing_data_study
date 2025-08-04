import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


options = Options()
options.add_argument('start-maximized')

driver = webdriver.Chrome(options=options)

driver.get("https://www.wildberries.ru/")

time.sleep(2)
# input = driver.find_element(By.XPATH, "//input[@id='searchInput']")
input = driver.find_element(By.ID, "searchInput")

input.send_keys("манга бсд")
input.send_keys(Keys.ENTER)

time.sleep(2)

while True:


    while True:
        wait = WebDriverWait(driver, 30)
        cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//article[@id]")))


        # cards = driver.find_elements(By.XPATH, "//article[@id]")    # 100
        # print(len(cards))
        count = len(cards)
        driver.execute_script("window.scrollBy(0,1500)")
        time.sleep(2)
        cards = driver.find_elements(By.XPATH, "//article[@id]")
        if len(cards) == count:
            break

    goods = {}
    anime_bsd_goods = []

    for card in cards:
        goods['price'] = card.find_element(By.XPATH, "//ins").text
        goods['name'] = card.find_element(By.XPATH, "./div/a").get_attribute('aria-label')
        goods['url'] = card.find_element(By.XPATH, "./div/a").get_attribute('href')
        anime_bsd_goods.append(goods)
        print(len(anime_bsd_goods))
        # TODO: save to database



    try:
        next_button = driver.find_element(By.XPATH, "//a[contains(@class, 'pagination-next')]")
        actions = ActionChains(driver)
        actions.move_to_element(next_button).click()
        actions.perform()
    except:
        break

print()