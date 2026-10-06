#!/usr/bin/env python3
"""Resolve art-direction catalogs into an integer-frame storyboard; no renderer."""
import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def catalog(filename, key):
    return json.loads((ROOT / 'assets' / filename).read_text(encoding='utf-8'))[key]


def resolve(items, query):
    matches = [item for item in items if query.casefold() in
               [str(item['id']).casefold(), str(item.get('name', '')).casefold(),
                *[str(a).casefold() for a in item.get('aliases', [])]]]
    if len(matches) != 1:
        raise ValueError(f'Expected one exact catalog match for {query!r}; use --catalog for IDs')
    return matches[0]


def allocate_frames(shares, total):
    """Largest-remainder allocation with at least one frame per beat."""
    if total < len(shares) or not all(math.isfinite(s) and s > 0 for s in shares):
        raise ValueError('Duration must fit every beat; shares must be finite and positive')
    remainder = total - len(shares)
    quotas = [s / sum(shares) * remainder for s in shares]
    frames = [1 + math.floor(q) for q in quotas]
    order = sorted(range(len(shares)), key=lambda i: (-(quotas[i] % 1), i))
    for i in order[:total - sum(frames)]:
        frames[i] += 1
    return frames


EDUCATION_BEATS = [
    {'id': 'question', 'share': .12, 'purpose': 'Ask one observable question'},
    {'id': 'model', 'share': .23, 'purpose': 'Introduce the model, quantities and assumptions'},
    {'id': 'mechanism', 'share': .40, 'purpose': 'Show the causal relationship with a computed model'},
    {'id': 'check', 'share': .17, 'purpose': 'Ask one understanding check; allow thinking time'},
    {'id': 'recap', 'share': .08, 'purpose': 'State the relationship and its limits'},
]


def build_plan(args):
    types = catalog('video-types.json', 'templates')
    education = args.education or args.type == 'science-explainer'
    template = ({'id': 'science-explainer', 'default_duration': 90, 'default_format': '9:16',
                 'default_style': 'minimal', 'default_motion': 'calm', 'beats': EDUCATION_BEATS}
                if args.type == 'science-explainer' else resolve(types, args.type))
    style = resolve(catalog('visual-styles.json', 'styles'), args.style or template['default_style'])
    motion = resolve(catalog('motion-profiles.json', 'motions'),
                     args.motion or ('calm' if education else template['default_motion']))
    formats = catalog('formats.json', 'formats')
    fmt_items = [dict(v, id=k) for k, v in formats.items()]
    fmt = resolve(fmt_items, args.format or ('9:16' if education else template['default_format']))
    seconds = args.seconds if args.seconds is not None else (90 if education else template['default_duration'])
    if not math.isfinite(seconds) or seconds <= 0 or args.fps <= 0:
        raise ValueError('Seconds and FPS must be finite and positive')
    total = math.floor(seconds * args.fps + .5)
    beats = EDUCATION_BEATS if education else template['beats']
    lengths = allocate_frames([b['share'] for b in beats], total)
    scenes, start = [], 0
    for beat, length in zip(beats, lengths):
        scenes.append(dict(beat, start_frame=start, end_frame=start + length,
                           start_seconds=start / args.fps, end_seconds=(start + length) / args.fps,
                           narration='', scientific_model='', labels=[], planned_holds=[]))
        start += length
    return {'schema_version': 1, 'renderer': 'fframes', 'fframes_version': '1.2.0',
            'brief': args.brief, 'education': education, 'seed': args.seed,
            'fps': args.fps, 'duration_frames': total, 'duration_seconds': total / args.fps,
            'width': fmt['width'], 'height': fmt['height'], 'format': fmt,
            'template_id': template['id'], 'style': style, 'motion': motion,
            'scenes': scenes, 'planned_holds': [], 'planned_black': [],
            'audio_required': False, 'review_status': 'draft',
            'notes': ['Catalog profiles are direction, not implemented FFrames effects.',
                      'Retime this draft after measuring narration; keep all frames accounted for.',
                      'Project rules, measured speech and physical models override preset pacing.']}


def storyboard(plan):
    text = [f"# Storyboard: {plan['template_id']}", '', plan['brief'], '',
            f"Draft: {plan['duration_frames']} frames at {plan['fps']} FPS. End frames are exclusive.",
            '', 'Replace all draft fields with the reviewed script and measured narration.']
    for scene in plan['scenes']:
        text += ['', f"## {scene['id']} ({scene['start_seconds']:.3f}–{scene['end_seconds']:.3f}s)"]
        for field in ['purpose', 'visual', 'camera', 'animation', 'typography', 'transition', 'audio']:
            text += [f"- {field.capitalize()}: {scene.get(field, '')}"]
        text += ['- Narration and captions:', '- Scientific model, units, assumptions and source:',
                 '- Labels and reading time:', '- Planned static holds / black intervals:',
                 '- Exit state and understanding check:']
    return '\n'.join(text) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', action='store_true')
    parser.add_argument('--type', default='science-explainer')
    parser.add_argument('--style')
    parser.add_argument('--motion')
    parser.add_argument('--format')
    parser.add_argument('--seconds', type=float)
    parser.add_argument('--fps', type=int, default=30)
    parser.add_argument('--seed', type=int, default=1)
    parser.add_argument('--education', action='store_true')
    parser.add_argument('--brief', default='')
    parser.add_argument('--output-dir', type=Path)
    args = parser.parse_args()
    try:
        if args.catalog:
            data = {key: sorted(i['id'] for i in catalog(file, field)) for key, file, field in
                    [('styles', 'visual-styles.json', 'styles'), ('motions', 'motion-profiles.json', 'motions'),
                     ('types', 'video-types.json', 'templates')]}
            data['types'].append('science-explainer')
            data['formats'] = list(catalog('formats.json', 'formats'))
            print(json.dumps(data, ensure_ascii=False, indent=2))
            return
        plan = build_plan(args)
        payload = json.dumps(plan, ensure_ascii=False, indent=2) + '\n'
        if args.output_dir:
            dest = args.output_dir.resolve()
            if dest == ROOT or ROOT in dest.parents:
                raise ValueError('Write project outputs outside the installed skill')
            if dest.exists():
                raise ValueError('Output directory already exists; choose a new draft location')
            dest.mkdir(parents=True)
            (dest / 'plan.json').write_text(payload, encoding='utf-8')
            (dest / 'storyboard.md').write_text(storyboard(plan), encoding='utf-8')
            print(dest)
        else:
            print(payload, end='')
    except (ValueError, KeyError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
