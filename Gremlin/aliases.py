import json

from utility import load_or_create_json


aliases = load_or_create_json('./aliases.json')


def add(keyword, replacement):
    aliases[keyword] = replacement
    with open('aliases.json', 'w') as outfile:
        json.dump(aliases, outfile, indent=4, default=str, sort_keys=True)


def list():
    listing = []
    for keyword in aliases:
        listing.append(f'{keyword}: {aliases[keyword]}')

    for item in sorted(listing):
        print(item)
        

def lookup(keyword):
    if keyword in aliases:
        return aliases[keyword]
    return None
