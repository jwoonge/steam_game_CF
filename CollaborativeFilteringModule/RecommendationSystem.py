import csv
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from CalculateUserVectors import get_game_data
import random

def recommend_CF(k, num_retrieve, train_set_g, test_set_g, train_set_t, test_set_t, game_datas, game_range, tag_range):
    num_test = len(test_set_g)
    game_range = np.array(game_range); tag_range = np.array(tag_range)
    recommend_rates = []
    for i in range(len(game_range)):
        game_id = game_range[i]
        recommend_rates.append(game_datas[game_id].recommend_rate)
    recommend_rates = np.array(recommend_rates)
    
    sim = cosine_similarity(test_set_t, train_set_t)
    sim_user_index = np.zeros((num_test, k))
    for i in range(num_test):
        arr = sim[i,:]
        idx = (-arr).argsort()[:k]
        sim_user_index[i,:] = idx.astype(int)

    recommend = []
    for i in range(num_test):
        temp = []
        count = 0
        sim_user = 0
        topn = 0
        while count<num_retrieve:
            sim_user_vector = train_set_g[int(sim_user_index[i][sim_user])]
            sim_user_vector = sim_user_vector * recommend_rates
            sim_user_vector_index = (-sim_user_vector).argsort()
            found_game_id = game_range[sim_user_vector_index[topn]]
            if not found_game_id in temp:
                temp.append(found_game_id)
                count += 1
            sim_user += 1
            if sim_user == k:
                topn += 1
                sim_user = 0
        recommend.append(temp)

    return recommend


def recommend_RD(k, test_set, game_range):
    recommended = []
    for i in range(len(test_set)):
        recommended.append(random.sample(game_range, k))
    return recommended

def recommend_TS(k, test_set):
    TopSellers = ['1174180','1313860','1118010','124923','1263850','1057090','1145360','728880','1091500','582010']
    recommended = []
    for i in range(len(test_set)):
        recommended.append(TopSellers[:k])
    return recommended

def normalize(vectors):
    mean_of_col = np.sum(vectors, axis=0)
    count_nonzero = np.count_nonzero(vectors, axis=0)
    count_nonzero = np.where(count_nonzero==0, 100, count_nonzero)
    mean_of_col = mean_of_col / count_nonzero
    mean_of_col = np.where(mean_of_col==0, 0.01, mean_of_col)
    return vectors / mean_of_col

if __name__=='__main__':
    ## Read Data & Normalize
    game_datas, game_range, tag_range = get_game_data('gamedata.txt')
    user_game_vectors = np.array(np.loadtxt('user_game_vectors.csv', dtype=np.float, delimiter=','))
    user_tag_vectors = np.array(np.loadtxt('user_tag_vectors.csv', dtype=np.float, delimiter=','))
    user_tag_vectors = normalize(user_tag_vectors)
    ## Separate test-train set
    test_size = 5
    test_set_g = user_game_vectors[:test_size, :]
    train_set_g = user_game_vectors[test_size:,:]
    test_set_t = user_tag_vectors[:test_size, :]
    train_set_t = user_tag_vectors[test_size:,:]
    ## Find most similar user by tag
    recommend_game_id = recommend_CF(5, train_set_g, test_set_g, train_set_t, test_set_t, game_datas, game_range, tag_range)
    origin_game_id = np.array(game_range)[(-test_set_g).argsort(axis=1)[:,:5]]

    for i in range(test_size):
        recommend_game_name = []
        recommend_game_tags = []
        origin_game_name = []
        origin_game_tags = []
        for j in range(len(recommend_game_id[i])):
            recommend_game_name.append(game_datas[recommend_game_id[i][j]].game_name)
            tags = ""
            for t in (game_datas[recommend_game_id[i][j]].tags):
                tags += t + '/'
            recommend_game_tags.append(tags)
        for j in range(len(origin_game_id[i])):
            origin_game_name.append(game_datas[origin_game_id[i][j]].game_name)
            tags = ""
            for t in (game_datas[origin_game_id[i][j]].tags):
                tags += t + '/'
            origin_game_tags.append(tags)
        print('==================================\nfor test user',i)
        print('who like to play')
        print('-------------------------------')
        for j in range(len(origin_game_name)):
            print('  - ',origin_game_name[j])
            print('\t\t',origin_game_tags[j],'\n')
        print('-------------------------------')
        print('we recommend')
        print('-------------------------------')
        for j in range(len(recommend_game_name)):
            print('  - ',recommend_game_name[j])
            print('\t\t',recommend_game_tags[j],'\n')
        