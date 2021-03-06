from bs4 import BeautifulSoup
import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import re

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
    

def click_view_page_btn(driver) :
    wait = WebDriverWait(driver,10)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[7]/div[4]/div/div[2]/div/div[1]/div[4]/a[1]')))
    element.click()



def get_game_data(url,driver,game_name) :
    print(url)
    driver.get(url)
    driver.implicitly_wait(3)
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    temp = url.split('/')
    game_id = temp[-1]
    print(game_name)
    print(game_id)
    temp = soup.select('.user_reviews_summary_row')
    try :
        if temp :
            if len(temp) <2 :
                if 'nonresponsive_hidden' in temp :
                    recent = temp[0].select('.nonresponsive_hidden')[0].text.replace(',','')
                    total = temp[0].select('.nonresponsive_hidden')[0].text.replace(',','')
                    recent_game_review = re.findall('\d+',recent)
                    total_game_review = re.findall('\d+',total)
                else :
                    recent_game_review = [0,0]
                    total_game_review = [0,0]
            else :
                recent = temp[0].select('.nonresponsive_hidden')[0].text.replace(',','')
                total = temp[1].select('.nonresponsive_hidden')[0].text.replace(',','')
                recent_game_review = re.findall('\d+',recent)[:2]
                total_game_review = re.findall('\d+',total)
            game_tag = []
            tags = soup.select('.app_tag')
        else :
            select_elementday = Select(driver.find_element_by_id("ageDay"))
            select_elementday.select_by_value('23')
            select_elementmonth = Select(driver.find_element_by_id("ageMonth"))
            select_elementmonth.select_by_value('February')
            select_elementyear = Select(driver.find_element_by_id("ageYear"))
            select_elementyear.select_by_value('1994')
            click_view_page_btn(driver)
            time.sleep(1)
            html = driver.page_source
            soup = BeautifulSoup(html,'html.parser')
            temp = soup.select('.user_reviews_summary_row')
            
            if len(temp) <2 :
                if 'nonresponsive_hidden' in temp :
                    recent = temp[0].select('.nonresponsive_hidden')[0].text.replace(',','')
                    total = temp[0].select('.nonresponsive_hidden')[0].text.replace(',','')
                    recent_game_review = re.findall('\d+',recent)
                    total_game_review = re.findall('\d+',total)
                else :
                    recent_game_review = [0,0]
                    total_game_review = [0,0]
                    
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
    except :
        recent_game_review = [0,0]
        total_game_review = [0,0]
        game_tag = ['None']

   

    write_game_data(game_name,game_id,recent_game_review,total_game_review,game_tag) 








options = webdriver.ChromeOptions()
#options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('resource/chromedriver_win32/chromedriver', chrome_options=options)
driver.implicitly_wait(3)
#test_url = ['https://store.steampowered.com/app/1257290/Atelier_Ryza_2_Lost_Legends__the_Secret_Fairy/']

#get_game_data(test_url,driver)

f = open('gamedata.txt','r',encoding='utf-8')
base_url='https://store.steampowered.com/app/'

for row in f :
    temp = row.split('##')
    urls = base_url + str(temp[0])
    get_game_data(urls,driver,temp[1])