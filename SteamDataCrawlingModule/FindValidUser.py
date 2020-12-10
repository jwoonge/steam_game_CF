from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

start_id = 76561197960265728
start_user = 0; end_user = 100000; num_user = 0
base_url = 'http://steamcommunity.com/profiles/'
file_dir = 'results/userdata/'
valid_user_list = open('results/valid_user_list.txt', 'a', encoding='utf-8')

options = webdriver.ChromeOptions()
#options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-gpu")
driver = webdriver.Chrome('resource/chromedriver_win32/chromedriver', chrome_options=options)
driver.implicitly_wait(3)

def get_valid_user(user_id, driver):
    url = base_url + str(user_id) + '/games?tab=all&sort=playtime/'
    driver.get(url)
    driver.implicitly_wait(3)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    game_list = soup.select('.gameListRowItem')
    if len(game_list)>0:
        
        return True
    else:
        if "made too many requests recentl" in html:
            return True
    return False

for user_i in range(start_user, end_user):
    user_id = start_id + start_user + user_i
    valid = get_valid_user(user_id, driver)
    if valid :
        num_user += 1
        valid_user_list.write(str(user_id)+'\n')
    print(user_i, " processed user ", str(start_id + start_user + user_i), valid, num_user)

valid_user_list.close()