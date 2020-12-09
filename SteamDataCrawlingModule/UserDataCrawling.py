from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

start_id = 76561197960265729

start_id = 76561198120029537 #for test
base_url = 'http://steamcommunity.com/profiles/'



def get_user_game_data(user_url, driver):
    all_game_url = user_url + 'games?tab=all&sort=playtime/'
    driver.get(all_game_url)
    driver.implicitly_wait(3)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    game_list = soup.select('.gameListRowItem')

    user_game_data = []
    for i in range(len(game_list)):
        game_name = game_list[i].select('.gameListRowItemName')[0].text
        game_playtime = game_list[i].select('.hours_played')[0].text
        if not game_playtime:
            game_playtime = 0 #.split()[0]
        else:
            game_playtime = float(game_playtime.split()[0])
        user_game_data.append(game_name, game_playtime)
    return user_game_data

def get_user_review_data(user_url, driver):
    all_review_data = user_url + 'reviews'

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('resource/chromedriver_win32/chromedriver', chrome_options=options)
driver.implicitly_wait(3)

for i in range(1):
    user_url = base_url + str(start_id+i) + '/'
    reviews_url = user_url + 'reviews'
    get_user_game_data(user_url, driver)

#https://steamcommunity.com/profiles/76561197960265728/ 사람 없음
#https://steamcommunity.com/profiles/76561197960265729/ 비공개됨
#https://steamcommunity.com/profiles/76561198120029537/ 공개됨


#/html/body/div[1]/div[7]/div[2]/div[1]/div[2]/div/div[5]/div[2]/div