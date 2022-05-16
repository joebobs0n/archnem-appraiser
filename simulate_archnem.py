#!/usr/bin/python3

import json, random
import argparse as ap
from pathlib import Path
from copy import deepcopy


def getArgs():
    args = ap.ArgumentParser(formatter_class=ap.MetavarTypeHelpFormatter)
    args.description = ''

    args.add_argument('-f', '--valuesfile', default='appraisal_data.json', type=Path,
                     help='File with all archnemesis modifier appraisals per rating. (Default=appraisal_data.json)')
    mods = args.add_mutually_exclusive_group()
    mods.add_argument('-m', '--n_mods', default=3, type=int,
                     help='Number of random mods to simulate. (Default=3)')
    mods.add_argument('-M', '--mods', default=None, nargs='+', type=str,
                      help='Space separated list of mods to simulate. For a list of valid mods, check src/empty_data.json. (Default=None)')

    return args.parse_args()

def getMultiplier(types):
    mult = []
    for t in set(deepcopy(types)):
        mult.append(types.count(t)-1)
    return sum(mult)


def simulate(data, mod_names):
    empty = {
        'base rating': 0,
        'synergy mult': 0,
        'final rating': 0,
        'tags': []
    }
    monster = {
        'archnames': mod_names,
        'mods': [],
        'AR': deepcopy(empty),
        'DR': deepcopy(empty),
        'BBR': deepcopy(empty)
    }
    for name in mod_names:
        monster['mods'].extend(data[name][0])

        for idx, rating in enumerate(['AR', 'DR', 'BBR'], start=1):
            monster[rating]['base rating'] += data[name][idx][0]
            types = [t for t in data[name][idx][1].split(',') if t != '']
            monster[rating]['tags'].extend(types)
    for rating in ['AR', 'DR', 'BBR']:
        monster[rating]['synergy mult'] = data['_SYNERGY_MULT']**getMultiplier(monster[rating]['tags'])
        monster[rating]['tags'].sort()
        monster[rating]['final rating'] = monster[rating]['base rating']*(monster[rating]['synergy mult'])
    print(json.dumps(monster, indent=2))

def main():
    args = getArgs()
    with open('appraisal_data.json', 'r') as f:
        data = json.load(f)

    valid_mods = [k for k in data.keys() if k[0] != '_']
    if args.mods == None:
        mod_names = random.sample(valid_mods, args.n_mods)
    else:
        mod_names = []
        for name in args.mods:
            if name.lower() in valid_mods:
                mod_names.append(name.lower())
            else:
                print(f'{name} not found in valid archnem mod list')
    simulate(data, mod_names)

if __name__ == '__main__':
    main()
