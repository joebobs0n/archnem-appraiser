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
    args.add_argument('-m', '--n_mods', default=3, type=int,
                     help='')
    args.add_argument('-s', '--n_sims', default=1, type=int,
                     help='')

    return args.parse_args()

def getMultiplier(types):
    mult = []
    for t in set(deepcopy(types)):
        mult.append(types.count(t)-1)
    return sum(mult)


def simulate(data, n_mods):
    mod_names = random.sample([k for k in data.keys() if k[0] != '_'], n_mods)
    monster = {
        'archnames': mod_names,
        'mods': [],
        'AR': [0,[],[]],
        'DR': [0,[],[]],
        'BBR': [0,[],[]]
    }
    for name in mod_names:
        monster['mods'].extend(data[name][0])

        for idx, rating in enumerate(['AR', 'DR', 'BBR'], start=1):
            monster[rating][0] += data[name][idx][0]
            types = [t for t in data[name][idx][1].split(',') if t != '']
            monster[rating][2].extend(types)
    for rating in ['AR', 'DR', 'BBR']:
        monster[rating][1] = getMultiplier(monster[rating][2])
        monster[rating][0] = monster[rating][0]*(data['_SYNERGY_MULT']**monster[rating][1])
    print(json.dumps(monster, indent=2))


def main():
    args = getArgs()
    with open('appraisal_data.json', 'r') as f:
        data = json.load(f)

    archnem_monsters = []
    for i in range(args.n_sims):
        archnem_monsters.append(simulate(data, args.n_mods))


if __name__ == '__main__':
    main()
