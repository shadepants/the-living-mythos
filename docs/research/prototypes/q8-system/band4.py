exec(open('band3.py').read().split('print("meatConv')[0])
import itertools
for mc, mh, g in itertools.product((300,),(0.01,0.015),(3.5,4.5)):
    globals().update(meatConv=mc, maxHunt=mh, gE=g)
    print(f"mc{mc} mh{mh} gE{g}: "+" || ".join(stats(m) for m in "BC"))
print("mild drought -0.45:")
for mh,g in ((0.01,3.5),(0.01,4.5)):
    globals().update(meatConv=300, maxHunt=mh, gE=g)
    _run=run
    def run(m,drought=(-0.45,8),**k): return _run(m,drought,**k)
    print(f"mh{mh} gE{g}: "+" || ".join(stats(m) for m in "BC")); run=_run
