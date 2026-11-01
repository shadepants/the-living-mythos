# Return-ordered allocation (prey choice by current per-worker return) instead of fixed rank, with prey depression.
import run3, sysproto_dep as S
S.meatConv = 40.0
def yield_ordered(Pm, Fm, L, target, ncell):
    rH = S.hMaxW*Fm/(Fm+S.hF); rG = S.gMaxW*Pm/(Pm+S.hP)
    capH = S.maxHunt*Fm*ncell*S.meatConv; capG = Pm*ncell*0.5
    meat = plant = 0.0; left = L
    for kind in sorted(('H','G'), key=lambda k: -(rH if k=='H' else rG)):
        need = target - meat - plant
        if need <= 0 or left <= 0: break
        if kind == 'H':
            meat = min(left*rH, capH, need); left -= meat/rH if rH > 0 else 0
        else:
            plant = min(left*rG, capG, need); left -= plant/rG if rG > 0 else 0
    return meat, plant
S.yield_at = yield_ordered
import sys
for cap,psi in [(0.2,float(a)) for a in sys.argv[1:]]:
    print(f"ordered cap {cap} psi {psi}: " + " || ".join(run3.run(s,cap,psi) for s in (1,2)))
