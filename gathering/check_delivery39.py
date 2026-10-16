#!/usr/bin/env python3
"""Validate Gathering 39's bytes, offline handoff, gallery and scope."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

from check_delivery import Gallery, jpeg_dimensions, png_dimensions


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    wall = Path('artifacts/gathering/wall-v19.png').read_bytes()
    assert wall == Path('artifacts/gathering/wall.png').read_bytes()
    assert png_dimensions(wall) == (1254, 1254)
    assert wall[24:26] == bytes((8, 2))
    jpg = Path('dist/gathering/39.jpg').read_bytes()
    assert jpeg_dimensions(jpg) == (512, 512) and len(jpg) < 100000
    record = json.loads(Path('dist/gathering/39.json').read_text())
    assert set(record) == {'name', 'image', 'attributes'}
    assert record['image'] == 'https://api.imd.fun/artifacts/' + hashlib.sha256(wall).hexdigest()
    attrs = {a['trait_type']: a['value'] for a in record['attributes']}
    assert len(attrs) == len(record['attributes']) == 6
    assert set(attrs) == {'Cave', 'Wall', 'Number', 'Left behind', 'Meaning', 'One thing'}
    assert attrs['Cave'] == 'Ice' and attrs['Wall'] == 'Gathering'
    assert type(attrs['Number']) is int and attrs['Number'] == 39
    assert attrs['One thing'] == 'Gathering'
    assert json.loads(Path('dist/goals.json').read_text()) == [
        {'line': i, 'goal': Path(f'line-{i}/GOAL.md').read_text().strip()} for i in range(1, 5)]

    content = Path('dist/index.html').read_text()
    gallery = Gallery(content)
    records = {p.relative_to('dist').as_posix(): json.loads(p.read_text())
               for p in Path('dist').glob('*/[0-9][0-9].json')}
    assert len(content.encode()) < 100000
    assert len(gallery.records) == len(records) == 195
    assert set(gallery.records) == set(records)
    assert len(gallery.images) == 95
    assert not set(gallery.tags) & {'script', 'iframe', 'link'}
    assert all(re.fullmatch(r'data:image/jpeg;base64,[A-Za-z0-9+/=]+', src)
               for src in gallery.images)
    for href in gallery.links:
        if href.startswith('#'):
            assert f'id="{href[1:]}"' in content
        elif not href.startswith('https://'):
            assert (Path('dist') / href).is_file(), href
    for name in ('gathering', 'line-1', 'line-2', 'line-3', 'line-4'):
        painted = [key for key in gallery.records if key.startswith(name + '/')
                   and records[key]['name'] != 'Not painted yet']
        assert painted == sorted(painted, reverse=True)
        for n in range(2, 22):
            p = Path('dist', name, f'{n:02}.json')
            assert json.loads(p.read_text()) == {
                'name': 'Not painted yet',
                'image': 'https://api.imd.fun/artifacts/b5e794cb2c70bd232230e389707698c69c2080786d606a13b39f9315c9a90799',
                'attributes': [{'trait_type': 'Cave', 'value': 'Ice'}]}
            assert not p.with_suffix('.jpg').exists()

    review = json.loads(Path('gathering/image-checks39.json').read_text())
    assert review['png']['sha256'] == hashlib.sha256(wall).hexdigest()
    assert review['visual_review_completed'] and review['unmet_visual_requirements'] == []
    assert digest('artifacts/gathering/wall-v18.png') == review['ancestor_sha256']
    assert json.loads(Path('dist/gathering/38.json').read_text())['image'].endswith(review['ancestor_sha256'])
    pixels = json.loads(subprocess.run(['node', '-e', """
const fs=require('node:fs'),{decode}=require('./gathering/thumbnail.js');
const a=decode(fs.readFileSync('artifacts/gathering/wall-v18.png'));
const b=decode(fs.readFileSync('artifacts/gathering/wall-v19.png'));
if(a.width!==b.width||a.height!==b.height||a.channels!==b.channels)throw Error('format changed');
let changed=0,outside=0;
for(let y=0;y<a.height;y++)for(let x=0;x<a.width;x++){
 const p=(y*a.width+x)*3;
 if(a.pixels[p]!==b.pixels[p]||a.pixels[p+1]!==b.pixels[p+1]||a.pixels[p+2]!==b.pixels[p+2]){
  changed++;if(x<420||x>510||y<920||y>1005)outside++;
 }
}
console.log(JSON.stringify({changed_pixels:changed,outside_rectangle_changed_pixels:outside}));
"""], capture_output=True, text=True, check=True).stdout)
    assert pixels['changed_pixels'] == review['preservation']['changed_pixels'] == 1161
    assert pixels['outside_rectangle_changed_pixels'] == 0

    tests = json.loads(Path('gathering/test-runs39.json').read_text())
    assert tests['ok'] and tests['line_tests'] == 709
    assert tests['shared_tests'] == 128 and tests['gathering_tests'] == 8
    assert tests['sources_unchanged_after_checks']
    trials = json.loads(Path('gathering/current-checks39.json').read_text())
    assert trials['ok'] and len(trials['results']) == 56
    assert all(row['passed'] for row in trials['results'])
    assert Path('gathering/COINS.md').read_text().splitlines()[0] == 'none'
    assert not Path('gathering/coin-order.json').exists()
    assert not Path('gathering/deploy-order.json').exists()

    source = Path('line-3/tools/import-origin-trace/origins.py').read_text().replace(
        "Path(__file__).resolve().parents[1] / 'import-budget' / 'budget.py'",
        "Path(__file__).resolve().with_name('budget.py')")
    assert source == Path('shared/import-drift/origins.py').read_text()
    source = Path('line-2/tools/csv-transitions/transitions.py').read_text()
    a = source.index('source = Path(__file__)')
    b = source.index('\n\ndef transitions', a)
    source = source[:a] + 'import reconcile as engine\n' + source[b:]
    assert source == Path('shared/import-drift/transitions.py').read_text()
    evidence = json.loads(Path('gathering/origin-evidence39.json').read_text())
    for item in evidence['inventory']['manifest']:
        assert digest(Path('shared/import-drift') / item['path']) == item['sha256']
    assert len(evidence['sites']) == 38 and not evidence['issues'] and not evidence['cycles']
    assert evidence['status_counts'] == {'resolved': 4, 'unresolved': 34}
    assert json.loads(Path('gathering/origin-review39.json').read_text())['comparison']['equal']
    repeat = subprocess.run(['python3', '-B', 'shared/import-drift/origin_csv.py',
        'compare', 'shared/import-drift/observed-origins39.csv',
        'shared/import-drift/observed-origins39.csv'], capture_output=True, text=True, check=True)
    assert json.loads(repeat.stdout) == json.loads(Path('gathering/origin-review39.json').read_text())

    roots = [Path(f'line-{i}') for i in range(1, 5)] + [Path(f'dist/line-{i}') for i in range(1, 5)]
    baseline = json.loads(Path('test/scratch/scope39.json').read_text())
    assert baseline == {str(p): digest(p) for root in roots for p in root.rglob('*') if p.is_file()}
    assert not subprocess.run(['git', 'diff', 'HEAD', '--', *map(str, roots)],
                              capture_output=True, check=True).stdout
    changed = subprocess.run(['git', 'diff', '--name-only', 'HEAD'],
                             capture_output=True, text=True, check=True).stdout.splitlines()
    added = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard'],
                           capture_output=True, text=True, check=True).stdout.splitlines()
    for name in set(changed + added):
        if name.startswith(('test/scratch/', 'artifacts/gathering/')):
            continue
        assert name.split('/')[0] in ('gathering', 'shared', 'dist'), name
        assert Path(name).is_file() and Path(name).stat().st_size < 100000, name
    tracked_outputs = subprocess.run(['git', 'ls-files', '--',
        'artifacts/gathering/wall-v19.png', 'artifacts/gathering/wall.png'],
        capture_output=True, text=True, check=True).stdout
    assert not tracked_outputs
    result = {'ok': True, 'png': review['png'], 'jpeg': review['jpeg'],
              'gallery_records': 195, 'painted_previews': 95, 'placeholders': 100,
              'gallery_bytes': len(content.encode()), 'line_paths_unchanged': True,
              'named_png_outputs_untracked': True, 'line_tests': 709,
              'shared_tests': 128, 'gathering_tests': 8, 'cli_trials': 56,
              'pixel_verification': pixels, 'unmet_visual_requirements': [],
              'independent_visual_certification': False}
    Path('gathering/delivery-checks39.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
