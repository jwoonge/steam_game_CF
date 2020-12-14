import csv
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from CalculateUserVectors import get_game_data

game_datas = get_game_data()
user_vectors = np.array(np.loadtxt('uservectors.csv', dtype=np.float, delimiter=','))
test_set = user_vectors[:5, :]
train_set = user_vectors[5:,:]
sim = cosine_similarity(test_set, train_set)
sim_user = np.argmax(sim, axis=1)

def most_sim_user_vector(train_set, test_set):
    sim = cosine_similarity(test_set, train_set)
    sim_user_index = np.argmax(sim, axis=1)
    return train_set[sim_user_index]

test_set_t = np.array([[0,0,1], [1,0,0], [0,1,1]])
train_set_t = np.array([[0,0,5], [1,1,0], [1,1,1], [0,1,2]])

sim_user = most_sim_user_vector(train_set_t, test_set_t)
print(sim_user)

#print(cos_sim(train_set, test_set.T))