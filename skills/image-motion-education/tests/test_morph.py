"""Numerical/CLI checks for facial interpolation; no production artwork or video."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'scripts/morph_rgba_pair.py'
AVAILABLE=importlib.util.find_spec('cv2') is not None and importlib.util.find_spec('numpy') is not None
if AVAILABLE:
    import numpy as np
    spec=importlib.util.spec_from_file_location('morph_helper',SCRIPT)
    helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)

@unittest.skipUnless(AVAILABLE,'Optional requirements-flow.txt is not installed')
class MorphTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup);self.work=Path(tmp.name)
        for name,shift in [('a',0),('b',4)]:
            im=Image.new('RGBA',(128,128));d=ImageDraw.Draw(im)
            d.ellipse((12,12,115,115),fill=(240,185,70,255))
            for x in [38,78]:
                d.ellipse((x,44,x+18,68),fill='white')
                d.ellipse((x+5+shift,49,x+10+shift,61),fill='black')
            im.save(self.work/f'{name}.png')
    def run_cli(self,out,*extra):
        return subprocess.run([sys.executable,str(SCRIPT),str(self.work/'a.png'),str(self.work/'b.png'),str(out),'--frames','5','--canvas-width','128','--canvas-height','128','--target-height','112','--bottom','120',*extra],text=True,capture_output=True)
    def test_exact_endpoints_and_stable_identical_pose(self):
        a=np.array(Image.open(self.work/'a.png'));b=np.array(Image.open(self.work/'b.png'))
        zero=np.zeros((128,128,2),dtype=np.float32)
        np.testing.assert_array_equal(helper.morph(a,b,zero,zero,0),a)
        np.testing.assert_array_equal(helper.morph(a,b,zero,zero,1),b)
        for t in [.1,.5,.9]:
            difference=np.abs(helper.morph(a,a,zero,zero,t).astype(int)-a.astype(int))
            self.assertLessEqual(difference.max(),1)
    def test_hidden_transparent_rgb_does_not_pollute_edges(self):
        a=np.zeros((64,64,4),dtype=np.uint8);a[:,:,:3]=[0,255,0]
        a[16:48,16:48]=[255,0,0,255]
        b=a.copy();b[:16,:,:3]=[0,0,255]
        forward=np.zeros((64,64,2),dtype=np.float32);forward[:,:,0]=1.5
        result=helper.morph(a,b,forward,-forward,.5)
        visible=result[:,:,3]>2
        self.assertGreater(int(visible.sum()),0)
        self.assertLessEqual(int(result[:,:,:3][visible][:,1:].max()),1)
        self.assertGreaterEqual(int(result[:,:,:3][visible][:,0].min()),253)
    def test_real_flow_cli_outputs_alpha_endpoints_and_provenance(self):
        out=self.work/'flow';r=self.run_cli(out);self.assertEqual(r.returncode,0,r.stderr)
        files=sorted(out.glob('morph-*.png'));self.assertEqual(len(files),5)
        expected=[helper.normalize(self.work/f'{name}.png',128,128,112,120) for name in ['a','b']]
        for p,e in zip([files[0],files[-1]],expected):
            np.testing.assert_array_equal(np.array(Image.open(p)),e)
        mid=np.array(Image.open(files[2]));self.assertEqual(mid.shape,(128,128,4))
        self.assertEqual(int(mid[0,0,3]),0)
        self.assertFalse(np.array_equal(mid,expected[0]))
        self.assertFalse(np.array_equal(mid,expected[1]))
        record=json.loads((out/'morph.json').read_text())
        self.assertEqual(record['frames_including_endpoints'],5)
        self.assertEqual(len(record['inputs'][0]['sha256']),64)
        self.assertTrue(record['versions']['opencv'])
    def test_existing_output_is_preserved(self):
        out=self.work/'flow';out.mkdir();sentinel=out/'morph-000.png';sentinel.write_bytes(b'approved')
        result=self.run_cli(out);self.assertNotEqual(result.returncode,0)
        self.assertEqual(sentinel.read_bytes(),b'approved');self.assertEqual(len(list(out.iterdir())),1)
    def test_mismatched_canvases_and_empty_states_fail(self):
        Image.new('RGBA',(64,64)).save(self.work/'b.png')
        result=self.run_cli(self.work/'bad');self.assertNotEqual(result.returncode,0)
        self.assertFalse((self.work/'bad').exists())
        Image.new('RGBA',(128,128)).save(self.work/'empty.png')
        with self.assertRaisesRegex(ValueError,'fully transparent'):
            helper.normalize(self.work/'empty.png',128,128,112,120)
        with self.assertRaises(ValueError):helper.normalize(self.work/'a.png',0,128,112,120)

if __name__=='__main__':unittest.main()
