##'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=XXXXXXXXXXXXXXXXX&steamid=76561197960434622&format=json'
import requests
from bs4 import BeautifulSoup

key = '33C798A71E856B20EC314196A31C6AB6'
start_user = 1000; end_user=20000; num_user = 0
file_dir = 'results/userdatatest'

valid_user_list = open('results/valid_user_list.txt', 'a', encoding='utf-8')

def get_user_game_data(user_id):
    url = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key='+key
    url += '&steamid='+user_id
    url += '&include_appinfo=true'
    url += '&include_played_free_games=true'
    url += '&format=json'
    json = requests.get(url).json()

    if 'response' in json and not len(json['response'].keys())==0: #valid user
        games = json['response']['games']
        userdata = []
        for game in games:
            game_id = game['appid']
            game_name = game['name']
            game_playtime = game['playtime_forever']
            userdata.append([game_id, game_name, game_playtime])
            
        userdata.sort(key=lambda x:x[2], reverse=True)
        return userdata, True

    else:
        return [], False

def write_user_game_data(user_id, game_data):
    f = open(file_dir + user_id + '.txt', 'w', encoding='utf-8')
    write_string = '@@ GAME\n'
    for gid, gname, gtime in game_data:
        write_string += str(gid) + ' ## ' + gname + '##' + str(gtime) + '\n'
    f.write(write_string)
    f.close()

for user_i in range(start_user, end_user):
    user_id = str(user_i + 76561198120029537)
    game_data, valid = get_user_game_data(user_id)
    if valid:
        valid_user_list.write(str(user_id)+'\n')
        write_user_game_data(user_id, game_data)


