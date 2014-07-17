#!/usr/bin/env python

import json

raw = json.loads(open('./latest_pretty.json').read())

nodes = []
edges = []
positions = []
links = []

names = {}
for item in raw:
    item['name'] = item['name'].replace('.', '-')
    names[item['name']] = item

front = {}
for item in raw:
    item['prereqs'] = [pre for pre in item['prereqs'] if pre in names]
    for pre in item['prereqs']:
        if pre not in front:
            front[pre] = []
        front[pre].append(item['name'])

frontier = [item['name'] for item in raw if not len(item['prereqs'])]
depth = {}

nxt = []
i = 0
while len(frontier):
    for name in frontier:
        depth[name] = i
        nxt += front.get(name, [])
    frontier = list(set(nxt))
    nxt = []
    i += 1
    if i > 100:
        print frontier
        break

weight = {}
waiting = names.keys()
while len(waiting):
    nxt = []
    for name in waiting[:]:
        w = []
        for pre in names[name]['prereqs']:
            if pre not in weight:
                break
            w += weight[pre] + [pre]
        else:
            weight[name] = list(set(w))
            waiting.remove(name)






for item in raw:
    nodes.append(item)
    item['size'] = len(weight[item['name']]) + 1 # 1 + len(item['prereqs'])
    item['depth'] = depth[item['name']]
    item['end'] = not len(front.get(item['name'], []))
    item['start'] = not len(item['prereqs'])
    item['x'] = item['h_position']
    item['y'] = item['v_position']
    item['connections'] =  weight[item['name']]
    for pre in item['prereqs']:
        pre = pre.replace('.', '-')
        if pre not in names:
            print "No source!", pre
            continue
        edges.append({
            'source': pre,
            'target': item['name'],
            'label': names[pre]['display_name'] + ' -> ' + item['display_name']
        })
        links.append({
            'source': raw.index(names[pre]),
            'target': raw.index(item),
            'label': names[pre]['display_name'] + ' -> ' + item['display_name']
        })
    positions.append({
        'name': item['name'],
        'label': item['display_name'],
        'display_name': item['display_name'],
        'x': item['h_position'],
        'y': item['v_position']
    })

open('./data.js', 'w').write('var data = ' + json.dumps({
    'nodes': nodes,
    'edges': edges,
    'links': links,
    'positions': positions
}, indent=2))


# vim: et sw=4 sts=4
