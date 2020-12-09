from bs4 import BeautifulSoup
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

base_url = 'https://store.steampowered.com/tags/en/Strategy/#p=0&tab=TopSellers'
def click_show_more_btn(driver):
        wait = WebDriverWait(driver,10)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, ' //*[@id="TopSellers_btn_next"]')))
        element.click()
        driver.implicitly_wait(1000)

def get_game_url(base_url,driver):
    urls = []
    game_id = dict()
    driver.get(base_url)
    driver.implicitly_wait(3)
    f = open('gamehtml.txt','w',encoding='utf-8')

    for j in range(10) :
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        rows = soup.select('#TopSellersRows')[0]
        url= rows.select('a')


        for i in range(len(url)) :
            urls.append(url[i]['href'])
            temp = url[i]['href'].split('/')
            print(temp)
        click_show_more_btn(driver)

    






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
#options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('resource/chromedriver_win32/chromedriver', chrome_options=options)
driver.implicitly_wait(3)

get_game_url(base_url,driver)

#https://steamcommunity.com/profiles/76561197960265728/ 사람 없음
#https://steamcommunity.com/profiles/76561197960265729/ 비공개됨
#https://steamcommunity.com/profiles/76561198120029537/ 공개됨


#/html/body/div[1]/div[7]/div[2]/div[1]/div[2]/div/div[5]/div[2]/div