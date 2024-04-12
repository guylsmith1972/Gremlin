import json


config = None

def get_config(path):
    global config
    if config is None:
        with open('config.json') as infile:
            config = json.load(infile)
            
    def lookup_part(conf, parts):
        if len(parts) == 0:
            return None
        if len(parts) == 1:
            return conf[parts[0]]
        else:
            return lookup_part(conf[parts[0]], parts[1:])
        
    parts = path.split('.')

    return lookup_part(config, parts)
            