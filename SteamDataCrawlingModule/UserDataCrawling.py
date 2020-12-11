from bs4 import BeautifulSoup
import requests
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

key = '33C798A71E856B20EC314196A31C6AB6'
file_no = 0
src_dir = 'results/validusers/'
dst_dir = 'results/userdata/'
base_url = 'http://steamcommunity.com/profiles/'

def get_user_game_data(user_id):
    url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key='+key
    url += '&steamid='+user_id
    url += '&include_appinfo=true'
    url += '&include_played_free_games=true'
    url += '&format=json'
    try :
        json = requests.get(url).json()

        if 'response' in json and not len(json['response'].keys())==0: #valid user
            try:
                games = json['response']['games']
                userdata = []
                for game in games:
                    game_id = game['appid']
                    game_name = game['name']
                    game_playtime = game['playtime_forever']
                    userdata.append([game_id, game_name, game_playtime])
                
                userdata.sort(key=lambda x:x[2], reverse=True)
                return userdata, True
            
            except:
                print(json)
                return [], False

        else:
            print(json)
            return [], False
    except:
        print('API ERROR')
        return [], False

def get_user_review_data(user_id, driver):
    review_url = base_url + user_id + '/reviews'
    driver.get(review_url)
    driver.implicitly_wait(3)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    review_list = soup.select('.review_box_content')
    user_review_data = []
    for i in range(len(review_list)):
        game_id = (review_list[i].select('.leftcol')[0].select('a')[0]['href'].split('/')[-1])
        recommend = review_list[i].select('.rightcol')[0].select('.title')[0].text
        user_review_data.append([game_id, recommend])
    return user_review_data

def write_user_data_file(game_data, review_data, user_id):
    f = open(dst_dir + user_id + '.txt','w', encoding='utf-8')
    write_string = '@@GAME\n'
    for game_id, game_name, game_playtime in game_data:
        write_string += str(game_id) + '##' + game_name + '##' + str(game_playtime) + '\n'
    write_string += '@@REVIEW\n'
    for game_id, recommend in review_data:
        write_string += game_id + '##' + recommend + '\n'
    f.write(write_string)
    f.close()

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-gpu")
driver = webdriver.Chrome('resource/chromedriver_win32/chromedriver', chrome_options=options)
driver.implicitly_wait(3)

collected_data = 0; row_index = 0
valid_user_list = open(src_dir+'user_list_'+str(file_no)+'.txt', 'r', encoding='utf-8')
for row in valid_user_list:
    user_id = row[:-1]
    user_game_data, valid = get_user_game_data(user_id)
    time.sleep(20)
    if valid:
        collected_data += 1
        user_review_data = get_user_review_data(user_id, driver)
        time.sleep(20)
        write_user_data_file(user_game_data, user_review_data, user_id)
    row_index += 1
    print(row_index, user_id,'processed')