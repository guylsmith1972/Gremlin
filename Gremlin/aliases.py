import json

from utility import load_or_create_json


aliases = load_or_create_json('./aliases.json', {})


def add(keyword, replacement):
    aliases[keyword] = replacement
    save_aliases()


def get_all():
    return aliases


def lookup(keyword):
    if keyword in aliases:
        return aliases[keyword]
    return None


def print_to_console():
    listing = []
    for keyword in aliases:
        listing.append(f'{keyword}: {aliases[keyword]}')

    for item in sorted(listing):
        print(item)
        

def remove(alias):
    if alias in aliases:
        del aliases[alias]
        save_aliases()
        
def save_aliases():
    with open('aliases.json', 'w') as outfile:
        json.dump(aliases, outfile, indent=4, default=str, sort_keys=True)