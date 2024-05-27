import json
from types import SimpleNamespace

def load_config(path='KGAT/parser/config.json'):
    with open(path, 'r') as file:
        data = json.load(file)
        return SimpleNamespace(**data)

def parse_kgat_args():
    args = load_config()

    # 계산된 경로 추가
    save_dir = f'trained_model'
    args.save_dir = save_dir

    return args