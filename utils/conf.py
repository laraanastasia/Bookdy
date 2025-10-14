import os
import yaml
def load_config(path: str = "configs/config.yaml") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()
    for k, v in os.environ.items():
        raw = raw.replace(f"${{{k}}}", v)
    return yaml.safe_load(raw)