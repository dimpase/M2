#!/usr/bin/env python3
"""Check cases where double starting approximations cannot suffice."""
import os
import subprocess
import sys
import tempfile
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
from benchmark import fromroots, parse

binary=str(Path(sys.argv[1] if len(sys.argv)>1 else './roots').resolve())
mp.mp.prec=4096
cases={
    'sub-double-separation': [(F(1),0),(1+F(1,2**100),0)],
    'outside-double-range': [(F(2)**1500,0),(F(2)**-1500,0)],
    'complex-multiplicity': [(F(1),F(2))]*4 + [(F(-2),F(1))]*3,
}
with tempfile.TemporaryDirectory(prefix='flint-machine-start-') as d:
    for name,expected in cases.items():
        a=fromroots(expected); p=Path(d)/name
        p.write_text(f'{len(a)-1} 150 exact 150\n'+''.join(f'{r} {i}\n' for r,i in a))
        run=subprocess.run([binary,'flint',str(p),'1'],capture_output=True,text=True,
                           timeout=45,check=True,env=dict(os.environ,M2_FLINT_ROOTS_TRIALS='1'))
        stats,roots=parse(run.stdout)
        assert len(roots)==len(expected)
        for re,im in expected:
            re,im=F(re),F(im)
            z=mp.mpc(mp.mpf(re.numerator)/re.denominator,mp.mpf(im.numerator)/im.denominator)
            j=min(range(len(roots)),key=lambda j:abs(roots[j]-z))
            error=abs(roots.pop(j)-z)/abs(z)
            assert error < mp.mpf(2)**-148,(name,error)
        assert all(int(line.split()[2])>=150 for line in run.stdout.splitlines()[1:])
        print(f"PASS {name}: {stats['workprec']} working bits",flush=True)
