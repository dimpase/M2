#!/usr/bin/env python3
"""Reproducible standalone comparison; each invocation warms up, then times 3 solves."""
import argparse, json, os, subprocess, time, random
from pathlib import Path
from fractions import Fraction as F
import mpmath as mp

def mul(a,b):
    c=[(F(0),F(0)) for _ in range(len(a)+len(b)-1)]
    for i,(ar,ai) in enumerate(a):
        for j,(br,bi) in enumerate(b):
            cr,ci=c[i+j];c[i+j]=(cr+ar*br-ai*bi,ci+ar*bi+ai*br)
    return c

def fromroots(xs):
    p=[(F(1),F(0))]
    for re,im in xs:p=mul(p,[(-F(re),-F(im)),(F(1),F(0))])
    return p

def real(a):return [(F(x),F(0)) for x in a]
def cases():
    rng=random.Random(4725)
    yield 'constant',real([7]),'exact',53
    yield 'zero-root-12',real([0]*12+[1]),'exact',53
    doc=real([1,1,0,0,7,0,0,0,0,5,0,0,0,1])
    yield 'doc-13',doc,'exact',53
    yield 'doc-square-26',mul(doc,doc),'exact',150
    yield 'wilkinson-20',fromroots([(j,0) for j in range(1,21)]),'exact',53
    yield 'cluster-12',fromroots([(1+F(j,2**30),0) for j in range(12)]),'exact',150
    yield 'complex-repeat-12',fromroots([(1,2)]*4+[(-2,1)]*3+[(0,-1)]*5),'mpfr',150
    yield 'wide-scale-10',fromroots([(F(2)**j,0) for j in range(-40,41,10)]+[(0,0)]),'exact',150
    for n in [32,100,256]:
        a=real([rng.randint(-100,100) for _ in range(n)]+[1])
        yield f'integer-{n}',a,'exact',53
        if n<=100:yield f'integer-{n}-256',a,'exact',256
    yield 'rational-32',real([F(rng.randint(-20,20),rng.randint(1,20)) for _ in range(32)]+[1]),'exact',150
    for kind in ['double','mpfr']:
        n=32
        a=[(F(rng.randint(-100,100),128),F(rng.randint(-100,100),128)) for _ in range(n)]+[(F(1),F(0))]
        yield 'complex-'+kind,a,kind,53 if kind=='double' else 150
        yield 'real-'+kind,real([F(rng.randint(-100,100),128) for _ in range(n)]+[1]),kind,53 if kind=='double' else 150
    yield 'roots-of-unity-256',real([-1]+[0]*255+[1]),'exact',53

def parse(text):
    lines=text.splitlines();h=lines[0].split()
    roots=[mp.mpc(*line.split()[:2]) for line in lines[1:]]
    return dict(seconds=float(h[1]),preprocess=float(h[3]),workprec=int(h[5]),count=int(h[7])),roots

def residual(a,z):
    f=mp.mpc(0);scale=mp.mpf(0)
    for re,im in reversed(a):
        c=mp.mpc(mp.mpf(re.numerator)/re.denominator,mp.mpf(im.numerator)/im.denominator)
        f=f*z+c;scale=scale*abs(z)+abs(c)
    return abs(f)/scale if scale else abs(f)

def agreement(a,b):
    # Match full multisets, retaining multiplicities; exact counts checked separately.
    remaining=list(b);worst=mp.mpf(0)
    for z in a:
        j=min(range(len(remaining)),key=lambda j:abs(z-remaining[j]))
        w=remaining.pop(j);worst=max(worst,abs(z-w)/max(abs(z),mp.mpf(1)))
    return float(-mp.log(worst,2)) if worst else 9999

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--binary',default='/tmp/flint-roots-prototype');ap.add_argument('--output',type=Path,required=True);ap.add_argument('--timeout',type=int,default=90);args=ap.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    results=[]
    for name,a,kind,bits in cases():
        mp.mp.prec=bits+200
        inp=args.output/(name+'.txt');inp.write_text(f'{len(a)-1} {bits} {kind} {bits}\n'+''.join(f'{r} {i}\n' for r,i in a))
        row=dict(case=name,degree=len(a)-1,bits=bits,kind=kind);rootsets={}
        for backend,threads in [('flint',1),('mps',1),('mps',8)]:
            label=f'{backend}-{threads}'
            try:
                r=subprocess.run([args.binary,backend,str(inp),str(threads)],capture_output=True,text=True,timeout=args.timeout,env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1'))
                (args.output/(name+'-'+label+'.log')).write_text(r.stdout+r.stderr)
                if r.returncode: row[label]=dict(error=r.stderr[-1000:],returncode=r.returncode)
                else:
                    stats,roots=parse(r.stdout);row[label]=stats;rootsets[label]=roots
                    stats['count_ok']=len(roots)==len(a)-1
                    stats['max_scaled_residual']=float(max((residual(a,z) for z in roots),default=0))
            except subprocess.TimeoutExpired:row[label]=dict(error=f'timeout {args.timeout}s (4 solves)')
            print(name,label,row[label],flush=True)
        if 'flint-1' in rootsets:
            for label in ['mps-1','mps-8']:
                if label in rootsets and len(rootsets[label])==len(rootsets['flint-1']):row[label]['agreement_bits']=agreement(rootsets['flint-1'],rootsets[label])
        results.append(row);(args.output/'results.json').write_text(json.dumps(results,indent=2))
if __name__=='__main__':main()
