import yaml


def load_config() -> dict:
    with open("config.yml", "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config
