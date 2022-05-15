#!/usr/bin/python3

import json
from copy import deepcopy



def main():
    with open('raw_data.json', 'r') as f:
        raw = json.load(f)
    with open('appraisal_data.json', 'r') as f:
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
                    [int(input('AR: ')), input('AR Type: ').lower()],
                    [int(input('DR: ')), input('DR Type: ').lower()],
                    [int(input('BRR: ')), input('BRR Type: ').lower()]
                ]
                appraisal[name] = deepcopy(temp)
                print('\n')

            with open('appraisal_data.json', 'w') as f:
                f.write(json.dumps(appraisal, indent=2))
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
