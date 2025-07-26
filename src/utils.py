import os

def _set_env(enviroment_key: str):
    if not os.environ.get(enviroment_key):
        os.environ[enviroment_key] = os.getenv(enviroment_key, '')
    return
