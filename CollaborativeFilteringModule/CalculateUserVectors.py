import os
import csv
from collections import namedtuple
MAXV = 999999
user_data_dir = '../SteamDataCrawlingModule/results/userdata/'

def get_game_data(filename='gamedata.txt'):
    game_datas = dict()
    f = open(filename, 'r',encoding='utf-8')
    game_tag_range = set()
    for row in f:
        game_id, game_name, avg_playtime, score, tags = row.split('##')
        avg_playtime = float(avg_playtime)
        score = float(score)
        tags = tags[:-1].split('$$')
        game_tag_range = game_tag_range.union(set(tags))
        tmp = namedtuple('game_data',['game_name', 'avg_playtime','recommend_rate', 'tags'])
        tmp.game_name = game_name; tmp.avg_playtime = avg_playtime; tmp.recommend_rate = score; tmp.tags = tags
        game_datas[game_id] = tmp
    game_tag_range.remove('')
    f.close()
    return game_datas, list(game_datas.keys()), list(game_tag_range)

def get_user_dict(user_id, game_datas):
    user_game_dict = dict()
    user_tag_dict = dict()
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
                if game_id in game_datas:
                    game_tags = game_datas[game_id].tags
                    for tag in game_tags:
                        if tag in user_tag_dict:
                            user_tag_dict[tag] += game_playtime
                        else:
                            user_tag_dict[tag] = game_playtime
                user_game_dict[game_id] = game_playtime
            else:
                game_id, rec = row.split('##')
                if 'Not' in rec:
                    user_game_dict[game_id] = - MAXV
                else:
                    user_game_dict[game_id] = MAXV
    return user_game_dict, user_tag_dict

def cal_user_game_vector(user_game_dict, game_range):
    user_game_vector = []
    vector_max = 0
    for game_id in game_range:
        if game_id in user_game_dict:
            if user_game_dict[game_id] == MAXV:
                user_game_vector.append(MAXV)
            elif user_game_dict[game_id] == -MAXV:
                user_game_vector.append(-5)
            else:
                value = user_game_dict[game_id] / game_datas[game_id].avg_playtime
                if value > vector_max:
                    vector_max = value
                user_game_vector.append(value)
        else:
            user_game_vector.append(0)
    for i in range(len(user_game_vector)):
        if user_game_vector[i]==MAXV:
            user_game_vector[i] = vector_max
    return user_game_vector

def cal_user_tag_vector(user_tag_dict, tag_range):
    user_tag_vector = []
    for tag in tag_range:
        if tag in user_tag_dict:
            user_tag_vector.append(user_tag_dict[tag])
        else:
            user_tag_vector.append(0)
    return user_tag_vector
        




if __name__=='__main__':
    game_datas, game_range, tag_range = get_game_data()
    gf = open('user_game_vectors.csv', 'w', newline='\n')
    tf = open('user_tag_vectors.csv', 'w', newline='\n')
    gw = csv.writer(gf)
    tw = csv.writer(tf)
    for filename in os.listdir(user_data_dir):
    #for filename in os.listdir(user_data_dir_test):
        user_id = filename[:-4]
        user_game_dict, user_tag_dict = get_user_dict(user_id, game_datas)
        user_game_vector = cal_user_game_vector(user_game_dict, game_range)
        user_tag_vector = cal_user_tag_vector(user_tag_dict, tag_range)
        print(user_tag_vector)
        gw.writerow(user_game_vector)
        tw.writerow(user_tag_vector)
    gf.close()
    tf.close()
