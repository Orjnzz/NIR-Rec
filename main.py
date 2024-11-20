import os
import random
from tqdm import tqdm
import pandas as pd
import numpy as np
from data_process import preprocess_data, sort_uf_items
from request import Request
from prompts import TEMPLATE_1, TEMPLATE_2, TEMPLATE_3
from utils import read_json, write_json
from config import init_config

# Khởi tạo cấu hình
config = init_config()

# Lấy API keys từ file cấu hình
api_keys = config["api_keys"]
model_name = config["model"]["name"]

# Tạo đối tượng Request
request_handler = Request(api_keys, model_name)

# Load data
data_ml_100k = read_json("./ml_100k.json")
user_matrix_sim, item_matrix_sim, u_item_dict, i_item_dict, i_item_id_list = preprocess_data(data_ml_100k)

# Variables
length_limit = config['data']['length_limit']
num_u = 12
total_i = config['data']['num_candidates']
random_seed = config['random_seed']
results_data = []
rank_list = []  # Danh sách để lưu rank của ground truth

# Candidate selection and  predictions
for i, elem in enumerate(tqdm(data_ml_100k[:1000], desc="Processing")):
    seq_list = elem[0].split(' | ')
    candidate_items = sort_uf_items(seq_list, user_matrix_sim[i], num_u=num_u, num_i=total_i)
    input_1 = TEMPLATE_1.format(', '.join(candidate_items), ', '.join(seq_list[-length_limit:]))

    # Step 1: Predict preferences
    predictions_1 = request_handler.request(user=input_1)
    input_2 = TEMPLATE_2.format(', '.join(candidate_items), ', '.join(seq_list[-length_limit:]), predictions_1)

    # Step 2: Select top movies
    predictions_2 = request_handler.request(user=input_2)
    input_3 = TEMPLATE_3.format(', '.join(candidate_items), ', '.join(seq_list[-length_limit:]), predictions_1, predictions_2)

    # Step 3: Recommend movies
    predictions = request_handler.request(user=input_3)
    hit_ = elem[1] in predictions

    # Calculate rank
    try:
        rank = predictions.index(elem[1]) + 1  # Rank starts at 1
    except ValueError:
        rank = len(predictions) + 1  # Nếu không có trong predictions, gán rank ngoài phạm vi

    rank_list.append(rank)

    # Collect results
    results_data.append({
        "PID": i,
        "Input_1": input_1,
        "Input_2": input_2,
        "Input_3": input_3,
        "GT": elem[1],
        "Predictions_1": predictions_1,
        "Predictions_2": predictions_2,
        "Predictions": predictions,
        "Hit": hit_,
        "Rank": rank
    })

# Kiểm tra và tạo thư mục 'results' nếu chưa tồn tại
os.makedirs("./results", exist_ok=True)

# Lưu kết quả chi tiết vào CSV
results_df = pd.DataFrame(results_data)
results_df["Hit"] = results_df["Hit"].astype(int)
results_df.to_csv(f"./results/results_len{length_limit}_cand{total_i}_seed{random_seed}.csv", index=False)

print("Processing complete. Results saved to CSV.")
