import numpy as np

def preprocess_data(data_ml_100k):
    u_item_dict, i_item_dict = {}, {}
    i_item_id_list = []
    u_item_p, i_item_p = 0, 0
    user_list, i_item_user_dict = [], {}

    for elem in data_ml_100k:
        seq_list = elem[0].split(' | ')
        for movie in seq_list:
            if movie not in u_item_dict:
                u_item_dict[movie] = u_item_p
                u_item_p += 1
            if movie not in i_item_user_dict:
                i_item_user_dict[movie] = [0.] * len(data_ml_100k)
                i_item_dict[movie] = i_item_p
                i_item_id_list.append(movie)
                i_item_p += 1
            i_item_user_dict[movie][data_ml_100k.index(elem)] += 1

    user_matrix = np.array([
        [1 if movie in elem[0].split(' | ') else 0 for movie in u_item_dict]
        for elem in data_ml_100k
    ])
    item_matrix = np.array([i_item_user_dict[movie] for movie in i_item_id_list])

    return (
        np.dot(user_matrix, user_matrix.T), 
        np.dot(item_matrix, item_matrix.T),  
        u_item_dict, i_item_dict, i_item_id_list
    )

def sort_uf_items(target_seq, user_sim, num_u, num_i):
    candidate_movies = {}
    sorted_users = sorted(enumerate(user_sim), key=lambda x: x[-1], reverse=True)[:num_u]
    weight_sum = sum(u[1] for u in sorted_users)

    for user_id, weight in sorted_users:
        weight /= weight_sum
        for movie in target_seq:
            if movie not in candidate_movies:
                candidate_movies[movie] = 0
            candidate_movies[movie] += weight
    return [movie for movie, _ in sorted(candidate_movies.items(), key=lambda x: -x[1])][:num_i]

def soft_if_items(target_seq, num_i, total_i, item_matrix_sim, item_dict):
    candidate_movies = {}
    for movie in target_seq:
        for idx, similarity in sorted(enumerate(item_matrix_sim[item_dict[movie]]), key=lambda x: -x[-1])[:num_i]:
            candidate_movie = item_dict[idx]
            if candidate_movie not in target_seq:
                candidate_movies[candidate_movie] = candidate_movies.get(candidate_movie, 0) + similarity
    return sorted(candidate_movies, key=candidate_movies.get, reverse=True)[:total_i]

def compute_user_item_similarity(user_matrix):
    return np.dot(user_matrix, user_matrix.T)
