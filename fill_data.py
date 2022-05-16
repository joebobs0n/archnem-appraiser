#!/usr/bin/python3

import json, os
import argparse as ap
from pathlib import Path
from copy import deepcopy



def getArgs():
    args = ap.ArgumentParser(formatter_class=ap.MetavarTypeHelpFormatter)
    args.description = ''

    args.add_argument('-i', '--infile', type=Path, default=None)
    args.add_argument('-o', '--outfile', type=Path, default='appraisal_data.json')

    return args.parse_args()

def main():
    args = getArgs()

    if args.infile != None and args.infile.exists():
        infile = args.infile
    elif Path('.autosave').exists():
        infile = Path('.autosave')
    else:
        infile = Path('src/empty.json')
    print(f'loading {infile}')

    with open('src/raw_data.json', 'r') as f:
        raw = json.load(f)
    with open(str(infile), 'r') as f:
        appraisal = json.load(f)

    try:
        for idx, item in enumerate(raw.items(), start=1):
            name, mods = item
            if appraisal[name] == []:
                # os.system('clear')
                print('\n', f'[{idx}/{len(raw)}] --- {name.upper()} '.ljust(80, '-'), '\n', sep='')
                print('\n'.join([f'  >> {m}' for m in mods]), '\n')
                temp = [
                    mods,
                    [int(input('AR: ')), input('AR Tags: ').lower()],
                    [int(input('DR: ')), input('DR Tags: ').lower()],
                    [int(input('BBR: ')), input('BBR Tags: ').lower()]
                ]
                appraisal[name] = deepcopy(temp)
                print('\n')

            with open('.autosave', 'w') as f:
                f.write(json.dumps(appraisal, indent=2))
        with open(str(args.outfile), 'w') as f:
            f.write(json.dumps(appraisal, indent=2))
        os.remove('.autosave')
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
