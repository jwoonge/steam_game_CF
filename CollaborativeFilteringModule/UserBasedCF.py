import csv
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from CalculateUserVectors import get_game_data
'''
def retrieve():
    return 추천하는 game_id
def evaluate():
    print(precision & recall)
'''

def normalize(vectors):
    mean_of_col = np.sum(vectors, axis=0)
    count_nonzero = np.count_nonzero(vectors, axis=0)
    count_nonzero = np.where(count_nonzero==0, 100, count_nonzero)
    mean_of_col = mean_of_col / count_nonzero
    mean_of_col = np.where(mean_of_col==0, 0.01, mean_of_col)
    return vectors / mean_of_col

def most_sim_user_index(train_set, test_set):
    sim = cosine_similarity(test_set, train_set)
    sim_user_index = np.argmax(sim, axis=1)
    return sim_user_index


game_datas, game_range, tag_range = get_game_data()
game_range = np.array(game_range); tag_range = np.array(tag_range)
recommend_rates = []
for i in range(len(game_range)):
    game_id = game_range[i]
    recommend_rates.append(game_datas[game_id].recommend_rate)
recommend_rates = np.array(recommend_rates)

## Read Data & Normalize
user_game_vectors = np.array(np.loadtxt('user_game_vectors.csv', dtype=np.float, delimiter=','))
user_tag_vectors = np.array(np.loadtxt('user_tag_vectors.csv', dtype=np.float, delimiter=','))
user_tag_vectors = normalize(user_tag_vectors)
## Separate test-train set
test_set_g = user_game_vectors[:5, :]
train_set_g = user_game_vectors[5:,:]
test_set_t = user_tag_vectors[:5, :]
train_set_t = user_tag_vectors[5:,:]
## Find most similar user
sim_user_index_t = most_sim_user_index(train_set_t, test_set_t)
print(sim_user_index_t)
sim_user_vector = train_set_g[sim_user_index_t]
sim_user_vector = sim_user_vector * recommend_rates


'''
sim_user_index_g = most_sim_user_index(train_set_g, test_set_g)
sim_user_vector_g = train_set_g[sim_user_index_g]
sim_user_vector_g = sim_user_vector_g * recommend_rates
'''
recommend_game_index = np.argmax(sim_user_vector, axis=1)
print(recommend_game_index)
recommand_game_id = game_range[recommend_game_index]
real_game_index = np.argmax(test_set_g, axis=1)
real_game_id = game_range[real_game_index]
print(recommand_game_id)
for i in range(len(recommand_game_id)):
    print('추천게임:',game_datas[recommand_game_id[i]].game_name)
    print('실제게임:',game_datas[real_game_id[i]].game_name)
    print('--')
    print(tag_range[np.argmax(test_set_t[i])])
