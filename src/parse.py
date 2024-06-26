from pathlib import Path
import yaml
import re

md = Path('Randomizers.md').read_text(encoding='UTF8')

series = dict()
current = 'OTHER'
subheading = None

def NewSeries(name):
    global series
    if series.get(name):
        return
    series[name] = {
        'name': name,
        'comment': '',
        'sub-series': [],
        'randomizers': [],
    }

NewSeries(current)

for line in md.splitlines():
    if line.startswith('## New randomizers'):
        current = 'New randomizers'
        NewSeries(current)

    if line.startswith('### '):
        current = line.replace('### ', '')
        subheading = None
        NewSeries(current)
        continue

    if line.startswith('#### '):
        subheading = line.replace('#### ', '')
        series[current]['sub-series'].append(subheading)
        continue

    if not line.startswith('- '):
        series[current]['comment'] += line
        continue
    
    m = re.match(r'^- \[(.+?)\]\((.+?)\)( \((.*?)\))?(.*)$', line)
    if not m:
        series[current]['randomizers'].append({
            'games': [None],
            'identifier': None,
            'url': None,
            'original': line
        })
        continue

    comment = m[5].replace('- _OBSOLETE_', '').strip()
    if comment.startswith('- '):
        comment = comment[2:]
    if comment.startswith('_') and comment.endswith('_'):
        comment = comment[1:-1]
    obsolete = '_OBSOLETE_' in m[5]

    data = {
        'games': m[1].split(' / '),
        'identifier': m[4],
        'url': m[2],
        #'original': line,
    }
    if subheading == 'Connected worlds':
        data['multiworld'] = True
    if subheading:
        data['sub-series'] = subheading
    if obsolete:
        data['obsolete'] = obsolete
    if comment:
        data['comment'] = comment

    series[current]['randomizers'].append(data)

for (k,v) in series.items():
    filename = re.sub(r'\s+', '_', k) + '.yml'
    file: Path = Path('dirty') / filename
    if isinstance(v, str):
        text = v
    else:
        if not v['comment']:
            v['comment'] = None
        if not v['sub-series']:
            v['sub-series'] = None
        text = yaml.dump(v, sort_keys=False, indent=4)
    file.write_text(text)