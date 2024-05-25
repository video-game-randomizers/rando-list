from pathlib import Path
import yaml
import re

md = Path('Randomizers.md').read_text(encoding='UTF8')

series = dict()
current = 'OTHER'
subheading = None

series[current] = {
    'name': current,
    'comment': '',
    'sub-series': [],
    'randomizers': [],
}

for line in md.splitlines():
    if line.startswith('### '):
        current = line.replace('### ', '')
        subheading = None
        if not series.get(current):
            series[current] = {
                'name': current,
                'comment': '',
                'sub-series': [],
                'randomizers': [],
            }
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
        series[current]['randomizers'].append({ 'original': line })
        continue

    comment = m[5].replace('- _OBSOLETE_', '').strip()
    obsolete = '_OBSOLETE_' in m[5]

    data = {
        'game': m[1],
        'url': m[2],
        'identifier': m[4],
        'original': line,
    }
    if subheading == 'Connected worlds':
        data['multiworld'] = True
    if subheading:
        data['subheading'] = subheading
    if obsolete:
        data['obsolete'] = obsolete
    if comment:
        data['comment'] = comment

    series[current]['randomizers'].append(data)

for (k,v) in series.items():
    filename = re.sub(r'\s+', '_', k) + '.yml'
    file: Path = Path('series') / filename
    if isinstance(v, str):
        text = v
    else:
        text = yaml.dump(v, sort_keys=False, indent=4)
    file.write_text(text)