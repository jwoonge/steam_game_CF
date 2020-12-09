from bs4 import BeautifulSoup
import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re

base_url = 'https://store.steampowered.com/tags/en/Strategy/#p=0&tab=TopSellers'
def write_game_data(game_name,game_id,recent,total,game_tag):

    filename = str(game_id) + '.txt'
    f = open('results/GameData/'+filename,'w',encoding='utf-8')
    write_string='@@Name'+'##'+str(game_name)+'\n'
    f.write(write_string)
    write_string='@@ID'+'##'+str(game_id)+'\n'
    f.write(write_string)
    write_string='@@Recent Review'+'##'+str(recent[0]) +'##'+str(recent[1]) +'\n'
    f.write(write_string)
    write_string='@@Total Review'+'##'+str(total[0]) +'##'+str(total[1]) +'\n'
    f.write(write_string)

    write_string='@@Tags'
    for i in range(len(game_tag)-1) :
        write_string+='##'+str(game_tag[i])
    write_string+='\n'
    f.write(write_string)

    f.close()  
    
def click_show_more_btn(driver):

        wait = WebDriverWait(driver,10)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, ' //*[@id="TopSellers_btn_next"]')))
        element.click()
       

def get_game_url(base_url,driver):
    urls = []
    driver.get(base_url)
    driver.implicitly_wait(3)

    for j in range(1000) :
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        rows = soup.select('#TopSellersRows')[0]
        url= rows.select('a')

        for i in range(len(url)) :
            urls.append(url[i]['href'])
        click_show_more_btn(driver)
        time.sleep(1)
    
    return urls

def get_game_data(urls,driver) :

    for i in urls :
        driver.get(i)
        driver.implicitly_wait(3)
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        temp = i.split('/')
        game_id = temp[4]
        game_name = soup.select('.apphub_AppName')[0].text
        temp = soup.select('.user_reviews_summary_row')
        if len(temp) <2 :
            recent = temp[0].select('.nonresponsive_hidden')[0].text.replace(',','')
            total = temp[0].select('.nonresponsive_hidden')[0].text.replace(',','')
            recent_game_review = re.findall('\d+',recent)
            total_game_review = re.findall('\d+',total)
        else :
            recent = temp[0].select('.nonresponsive_hidden')[0].text.replace(',','')
            total = temp[1].select('.nonresponsive_hidden')[0].text.replace(',','')
            recent_game_review = re.findall('\d+',recent)[:2]
            total_game_review = re.findall('\d+',total)
        game_tag = []
        tags = soup.select('.app_tag')

        for j in range(len(tags)) :
            temp = tags[j].text.replace('\t','')
            game_tag.append(temp.replace('\n',''))

        write_game_data(game_name,game_id,recent_game_review,total_game_review,game_tag) 








options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('resource/chromedriver_win32/chromedriver', chrome_options=options)
driver.implicitly_wait(3)

urls = get_game_url(base_url,driver)
get_game_data(urls,driver)

#https://steamcommunity.com/profiles/76561197960265728/ 사람 없음
#https://steamcommunity.com/profiles/76561197960265729/ 비공개됨
#https://steamcommunity.com/profiles/76561198120029537/ 공개됨


#/html/body/div[1]/div[7]/div[2]/div[1]/div[2]/div/div[5]/div[2]/div