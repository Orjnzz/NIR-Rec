import os
import yaml

def init_config():
    current_path = os.path.dirname(os.path.realpath(__file__))

    # Đọc file overall.yaml
    overall_file = os.path.join(current_path, './assets/overall.yaml')
    with open(overall_file, 'r') as file:
        overall_config = yaml.safe_load(file)

    # Đọc file openai.yaml
    openai_file = os.path.join(current_path, './assets/openai.yaml')
    with open(openai_file, 'r') as file:
        openai_config = yaml.safe_load(file)

    # Kết hợp cả hai cấu hình
    config = {**overall_config, **openai_config}

    return config