import json
from types import SimpleNamespace

def load_config(path='KGAT/parser/config.json'):
    with open(path, 'r') as file:
        data = json.load(file)
        return SimpleNamespace(**data)

def parse_kgat_args():
    args = load_config()

    # 계산된 경로 추가
    save_dir = f'trained_model/KGAT/{args.data_name}/embed-dim{args.embed_dim}_relation-dim{args.relation_dim}_{args.laplacian_type}_{args.aggregation_type}_{"".join([str(i) for i in eval(args.conv_dim_list)])}_lr{args.lr}_pretrain{args.use_pretrain}'
    args.save_dir = save_dir

    return args