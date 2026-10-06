#!/usr/bin/env python3
"""Regression tests for catalog resolution, frame budgets, and real FFmpeg QC."""
import argparse
import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / f'{name}.py')
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


plan = module('plan')
qc = module('qc')


class Helpers(unittest.TestCase):
    def args(self, **overrides):
        values = dict(type='science-explainer', education=False, style=None, motion=None,
                      format=None, seconds=None, fps=30, seed=7, brief='မြန်မာ')
        values.update(overrides)
        return argparse.Namespace(**values)

    def test_all_catalogs_resolve_and_budget_is_exact(self):
        self.assertEqual(len(plan.catalog('visual-styles.json', 'styles')), 51)
        self.assertEqual(len(plan.catalog('motion-profiles.json', 'motions')), 10)
        self.assertEqual(len(plan.catalog('video-types.json', 'templates')), 13)
        for entry in plan.catalog('video-types.json', 'templates'):
            draft = plan.build_plan(self.args(type=entry['id'], seconds=7.37))
            self.assertEqual(draft['scenes'][-1]['end_frame'], draft['duration_frames'])
            for a, b in zip(draft['scenes'], draft['scenes'][1:]):
                self.assertEqual(a['end_frame'], b['start_frame'])
        for file, key in [('visual-styles.json', 'styles'), ('motion-profiles.json', 'motions')]:
            for entry in plan.catalog(file, key):
                self.assertEqual(plan.resolve(plan.catalog(file, key), entry['id'])['id'], entry['id'])

    def test_teaching_override_unicode_and_invalid_budget(self):
        result = plan.build_plan(self.args(type='cinematic-trailer', education=True))
        self.assertEqual(result['motion']['id'], 'calm')
        self.assertEqual(result['brief'], 'မြန်မာ')
        self.assertEqual([s['id'] for s in result['scenes']], ['question', 'model', 'mechanism', 'check', 'recap'])
        with self.assertRaises(ValueError):
            plan.allocate_frames([1, 1], 1)
        with self.assertRaises(ValueError):
            plan.build_plan(self.args(seconds=float('nan')))

    def test_interval_union(self):
        allowed = [{'start_seconds': 0, 'end_seconds': 1}, {'start_seconds': 1, 'end_seconds': 2}]
        self.assertTrue(qc.covered((.1, 1.9), allowed, .01))
        self.assertFalse(qc.covered((.1, 3), allowed, .01))

    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'FFmpeg required')
    def test_encoded_media_and_audio_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            video = base / 'moving.mp4'
            qc.run(['ffmpeg', '-loglevel', 'error', '-nostdin', '-f', 'lavfi', '-i',
                    'testsrc2=size=320x180:rate=30:duration=2', '-f', 'lavfi', '-i',
                    'sine=frequency=440:duration=2', '-af', 'volume=0.2', '-c:v', 'libx264',
                    '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', str(video)])
            expected = {'width': 320, 'height': 180, 'fps': 30, 'duration_seconds': 2, 'audio_required': True}
            (base / 'qc').mkdir()
            result = qc.inspect(video, expected, base / 'qc')
            self.assertEqual(result['status'], 'review_required')
            self.assertTrue(all(c['status'] == 'pass' for c in result['checks']))
            self.assertTrue((base / 'qc/qc-sheet.jpg').is_file())
            self.assertEqual(len(result['sha256']), 64)
            silent = base / 'silent.mp4'
            qc.run(['ffmpeg', '-loglevel', 'error', '-nostdin', '-i', str(video), '-an', '-c:v', 'copy', str(silent)])
            (base / 'fail').mkdir()
            result = qc.inspect(silent, expected, base / 'fail')
            self.assertEqual(result['status'], 'fail')
            self.assertEqual(next(c['status'] for c in result['checks'] if c['name'] == 'audio_presence'), 'fail')


if __name__ == '__main__':
    unittest.main()
