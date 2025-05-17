import yaml
import logging.config


def init_logging(logging_config_path: str):
    with open(logging_config_path, "rt") as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
