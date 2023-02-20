import json
url = '../data/rocketguns/'

with open(f'{url}fr_r_550_magic.blkx', 'r') as f:
    lines = json.load(f)
    print(lines)
    print(lines['rocketGun'])


