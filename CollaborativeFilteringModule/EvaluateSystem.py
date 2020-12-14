import numpy as np
from CalculateUserVectors import get_game_data
from RecommendationSystem import *

def average_precision(recommended, relevant):
    MAP = 0
    for i in range(len(recommended)):
        AP = 0
        count = 0
        for j in range(len(recommended[i])):
            if recommended[i][j] in relevant:
                count += 1
                AP += count / (j+1)
        MAP += AP/len(relevant)
    MAP = MAP/len(recommended)
    return MAP




## Read Data & Normalize
game_datas, game_range, tag_range = get_game_data('gamedata.txt')
user_game_vectors = np.array(np.loadtxt('user_game_vectors.csv', dtype=np.float, delimiter=','))
user_tag_vectors = np.array(np.loadtxt('user_tag_vectors.csv', dtype=np.float, delimiter=','))
user_tag_vectors = normalize(user_tag_vectors)
num_total_users = len(user_game_vectors)
num_test_users = int(num_total_users * 0.2)
print('Read Data & Normalize Done')
## Separate test-train set
test_set_g = user_game_vectors[:num_test_users, :]
train_set_g = user_game_vectors[num_test_users:,:]
test_set_t = user_tag_vectors[:num_test_users, :]
train_set_t = user_tag_vectors[num_test_users:,:]
## Find most similar user by tag
recommended_game_id_CF = recommend_CF(10, train_set_g, test_set_g, train_set_t, test_set_t, game_datas, game_range, tag_range)
recommended_game_id_RD = recommend_RD(10, test_set_g, game_range)
recommended_game_id_TS = recommend_TS(10, test_set_g)
origin_game_ids = np.array(game_range)[(-test_set_g).argsort(axis=1)[:,:3]]

print('MAP score of CF :\t\t',average_precision(recommended_game_id_CF, origin_game_ids))
print('MAP score of Random :\t\t',average_precision(recommended_game_id_RD, origin_game_ids))
print('MAP score or TopSellers :\t',average_precision(recommended_game_id_TS, origin_game_ids))