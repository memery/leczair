
import json
from state import State, from_dict


def load_settings():
    with open('settings.json', 'r') as conf:
        return from_dict(json.load(conf))

def init():
    state = State()
    state.settings = load_settings() 
    
    load_settings(state.settings)


if __name__ == '__main__':
    init()


