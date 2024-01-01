import yaml

def load_mvmt_params() -> list[dict]:
    with open(r'params\mvmt.yaml', 'r') as yml:
        data = yaml.safe_load(yml)
    return data
