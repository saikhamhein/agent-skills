#!/usr/bin/env python3
"""Check encoded media, detect suspect intervals, and extract a final-file contact sheet."""
import argparse
import hashlib
import json
import math
import re
import subprocess
from fractions import Fraction
from pathlib import Path


def run(argv):
    result = subprocess.run(argv, capture_output=True, text=True, check=False)
    if result.returncode:
        raise RuntimeError(f'{argv[0]} failed: {result.stderr[-3000:]}')
    return result.stdout, result.stderr


def intervals(log, kind, duration):
    if kind == 'black':
        return [(float(a), float(b)) for a, b in re.findall(
            r'black_start:([\d.]+) black_end:([\d.]+)', log)]
    starts = [float(x) for x in re.findall(r'freeze_start: ([\d.]+)', log)]
    ends = [float(x) for x in re.findall(r'freeze_end: ([\d.]+)', log)]
    return [(a, ends[i] if i < len(ends) else duration) for i, a in enumerate(starts)]


def covered(interval, allowed, tolerance):
    """Accept only intervals completely covered by the union of planned ranges."""
    cursor, end = interval
    for item in sorted(allowed, key=lambda x: x['start_seconds']):
        a, b = item['start_seconds'], item['end_seconds']
        if not (math.isfinite(a) and math.isfinite(b) and 0 <= a <= b):
            raise ValueError('Planned intervals must be finite, ordered and nonnegative')
        if a > cursor + tolerance:
            continue
        if b >= cursor:
            cursor = max(cursor, b)
        if cursor >= end - tolerance:
            return True
    return False


def inspect(video, plan, out):
    raw, _ = run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(video)])
    probe = json.loads(raw)
    videos = [s for s in probe['streams'] if s['codec_type'] == 'video']
    audio = [s for s in probe['streams'] if s['codec_type'] == 'audio']
    if len(videos) != 1:
        raise ValueError('Expected exactly one video stream')
    stream = videos[0]
    duration = float(stream.get('duration', probe['format']['duration']))
    fps = float(Fraction(stream['avg_frame_rate']))
    tolerance = max(2 / plan['fps'], .1)
    checks = []
    def check(name, ok, actual):
        checks.append({'name': name, 'status': 'pass' if ok else 'fail', 'actual': actual})
    check('resolution', (stream['width'], stream['height']) == (plan['width'], plan['height']),
          [stream['width'], stream['height']])
    check('average_fps', abs(fps - plan['fps']) < .001, fps)
    check('duration', abs(duration - plan['duration_seconds']) <= tolerance, duration)
    check('audio_presence', bool(audio) or not plan.get('audio_required', False), bool(audio))
    _, log = run(['ffmpeg', '-hide_banner', '-nostdin', '-i', str(video), '-an', '-vf',
                  'blackdetect=d=0.25:pix_th=0.10,freezedetect=n=-50dB:d=1', '-f', 'null', '-'])
    suspects = []
    for kind, field in [('black', 'planned_black'), ('freeze', 'planned_holds')]:
        for a, b in intervals(log, kind, duration):
            expected = covered((a, b), plan.get(field, []), tolerance)
            suspects.append({'kind': kind, 'start_seconds': a, 'end_seconds': b,
                             'status': 'planned' if expected else 'review_required'})
    loudness = None
    if audio:
        _, soundlog = run(['ffmpeg', '-hide_banner', '-nostdin', '-i', str(video), '-vn', '-af',
                          'loudnorm=I=-16:TP=-1:LRA=11:print_format=json', '-f', 'null', '-'])
        blocks = re.findall(r'\{\s*"input_i"[\s\S]*?\}', soundlog)
        if not blocks:
            raise RuntimeError('FFmpeg did not return loudness measurements')
        loudness = json.loads(blocks[-1])
        peak = float(loudness['input_tp'])
        check('true_peak_ceiling', peak <= -1, loudness['input_tp'])
        # Silence is allowed only when audio is optional; never infer intelligibility from a number.
        check('required_audio_not_silent', not plan.get('audio_required', False)
              or math.isfinite(float(loudness['input_i'])), loudness['input_i'])
    # Review actual encoded frames, not SVG drafts. Space samples across the complete video.
    count = min(12, max(1, math.ceil(duration * fps)))
    sheet = out / 'qc-sheet.jpg'
    run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-nostdin', '-i', str(video), '-vf',
         f'fps={count / max(duration, .001)},scale=320:-2,tile=4x3:padding=8:margin=8:color=gray',
         '-frames:v', '1', str(sheet)])
    if not sheet.is_file():
        raise RuntimeError('Contact sheet was not created')
    manual = ['Inspect the full-resolution Burmese/other text and glyph shaping on the chosen backend.',
              'Review scientific models, units, sources, simplifications and understanding check.',
              'Watch the entire encoded video; check scene boundaries, pacing, safe areas and captions.',
              'Listen for narration intelligibility, clicks, music balance and caption sync.',
              'Read native FFrames inspect/timeline reports; encoded-file checks do not replace them.']
    status = ('fail' if any(c['status'] == 'fail' for c in checks) else 'review_required')
    with video.open('rb') as handle:
        digest = hashlib.file_digest(handle, 'sha256').hexdigest()
    return {'schema_version': 1, 'status': status, 'video': str(video), 'sha256': digest,
            'checks': checks, 'suspect_intervals': suspects, 'loudness': loudness,
            'contact_sheet': str(sheet), 'manual_reviews': manual,
            'limitations': ['Average FPS does not prove constant frame timing.',
                            'Black/freeze detection is heuristic; planned holds are valid.',
                            'No automatic scientific, language, clipping or aesthetic approval.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--video', type=Path, required=True)
    parser.add_argument('--plan', type=Path, required=True)
    parser.add_argument('--out-dir', type=Path, required=True)
    args = parser.parse_args()
    try:
        plan = json.loads(args.plan.read_text(encoding='utf-8'))
        for key in ('fps', 'duration_seconds', 'width', 'height'):
            if not isinstance(plan[key], (float, int)) or not math.isfinite(plan[key]) or plan[key] <= 0:
                raise ValueError(f'{key} must be finite and positive')
        out = args.out_dir.resolve()
        root = Path(__file__).resolve().parents[1]
        if out == root or root in out.parents or out.exists():
            raise ValueError('Use a fresh output directory outside the installed skill')
        out.mkdir(parents=True)
        report = inspect(args.video.resolve(), plan, out)
        (out / 'qc.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(json.dumps({'status': report['status'], 'report': str(out / 'qc.json')}))
        return 1 if report['status'] == 'fail' else 0
    except (ValueError, KeyError, OSError, RuntimeError, ZeroDivisionError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    raise SystemExit(main())
