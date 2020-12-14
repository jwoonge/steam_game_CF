import os
import csv
MAXV = 999999
user_data_dir = '../SteamDataCrawlingModule/results/userdata/'
user_data_dir_test = 'fortesting/'

def get_game_data(filename='gamedata.txt'):
    game_datas = dict()
    f = open(filename, 'r',encoding='utf-8')
    for row in f:
        game_id, game_name, avg_playtime, score = row.split('##')
        avg_playtime = float(avg_playtime[:-1])
        game_datas[game_id] = [game_name, avg_playtime, score]
    f.close()
    return game_datas

def get_user_dict(user_id):
    user_dict = dict()
    f = open(user_data_dir + user_id + '.txt', 'r', encoding='utf-8')
    GR = 'game'
    for row in f:
        if row=='@@GAME\n':
            pass
        elif '@@REVIEW' in row:
            GR = 'review'
        else:
            if GR == 'game':
                game_id, game_name, game_playtime = row.split('##')
                game_playtime = float(game_playtime[:-1])
                user_dict[game_id] = game_playtime
            else:
                game_id, rec = row.split('##')
                if 'Not' in rec:
                    user_dict[game_id] = -MAXV
                else:
                    user_dict[game_id] = MAXV
    return user_dict

def cal_user_vector(user_dict):
    vector = []
    vector_max = 0
    for game_id in game_range:
        if game_id in user_dict:
            if user_dict[game_id] == MAXV:
                vector.append(MAXV)
            elif user_dict[game_id] == -MAXV:
                vector.append(-5)
            else:
                value = user_dict[game_id] / game_datas[game_id][1]
                if value > vector_max:
                    vector_max = value
                vector.append(value)
        else:
            vector.append(0)
    for i in range(len(vector)):
        if vector[i]==MAXV:
            vector[i] = vector_max
    return vector

if __name__=='__main__':
    game_datas = get_game_data()
    game_range = list(game_datas.keys())
    f = open('uservectors.csv', 'w', newline='\n')
    w = csv.writer(f)
    #for filename in os.listdir(user_data_dir):
    for filename in os.listdir(user_data_dir_test):
        user_id = filename[:-4]
        user_dict = get_user_dict(user_id)
        user_vector = cal_user_vector(user_dict)
        w.writerow(user_vector)
    f.close()
