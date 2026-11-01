# Q13 probe: glance-word rule variants applied to dumped streams (q13run.py).
# args: pkl...   Prints, per variant: word shares (calm 200 yr / drought 60 yr), gaps, flicker,
# words shown by bands in the season before they migrate or end, and how often 'restless' coincides with starving.
# Throwaway; never port.
import sys, pickle, collections
FLAT, THRIVE_STASH, MIGRATE_AFTER, STARVING = 0.05, 0.4, 2, 2

def facts(rows):
    # per band: trend = mean of last 4 balances (already / consumption), stash ratio, restless
    hist = collections.defaultdict(list); out = []
    for r in sorted(rows, key=lambda r: (r['t'], r['band'])):
        if r.get('born'): continue
        h = hist[r['band']]; h.append(r['bal']); h[:] = h[-4:]
        tr = sum(h)/len(h)
        trend = 'rising' if tr > FLAT else 'falling' if tr < -FLAT else 'flat'
        act = r['act']; moved = bool(act) and act[0] == 'migrated'; ended = bool(act) and act[0] in ('dissolved', 'perished')
        out.append(dict(r, trend=trend, stashr=r['stash']/r['cons'] if r.get('cons') else 0.0,
                        restless=r['hungry'] >= MIGRATE_AFTER and not moved and not ended, moved=moved, ended=ended))
    return out

def word(f, var):
    starving, hungry = f['hungry'] >= STARVING, f['hungry'] >= 1
    thriving = f['trend'] == 'rising' and f['stashr'] >= THRIVE_STASH
    if var == 'draft':      # rough draft: restless first; rules as written in spec §16, no default
        if f['restless']: return 'restless'
        if starving: return 'starving'
        if hungry: return 'hungry'
        if thriving: return 'thriving'
        if f['trend'] == 'flat': return 'settled'
        return None         # gap: falling or rising-without-stash, not hungry
    if var == 'severity':   # same words, severity first; restless after hunger
        if starving: return 'starving'
        if hungry: return 'hungry'
        if f['restless']: return 'restless'
        if thriving: return 'thriving'
        if f['trend'] == 'flat': return 'settled'
        return None
    if var in ('effort', 'effort_hyst'):   # severity first; thriving = effort at or below effortFull (full fertility: growing)
        if starving: return 'starving'
        if hungry: return 'hungry'
        if var == 'effort': return 'thriving' if f['eff'] <= 0.5 else 'settled'
        return 'thriving' if f['eff'] <= f['_hyst_edge'] else 'settled'
    if var == 'ladder':     # severity first, full partition: 'lean' covers falling-not-hungry; settled is the default
        if starving: return 'starving'
        if hungry: return 'hungry'
        if f['trend'] == 'falling': return 'lean'
        if thriving: return 'thriving'
        return 'settled'

for var in ('draft', 'severity', 'ladder', 'effort', 'effort_hyst'):
    tot = collections.Counter(); pre = collections.Counter(); calm = collections.Counter(); dro = collections.Counter()
    flips = bandyrs = 0
    for p in sys.argv[1:]:
        d = pickle.load(open(p, 'rb')); burn = d['burn']; fs = facts(d['rows'])
        last = {}; prevrow = {}
        for f in fs:
            b = f['band']; f['_hyst_edge'] = 0.55 if last.get(b) == 'thriving' else 0.5
            w = word(f, var)
            if burn - 800 <= f['t'] < burn:
                calm[w] += 1; bandyrs += 0.25
                if b in last and last[b] != w: flips += 1
            elif burn <= f['t'] < burn + 240: dro[w] += 1
            if f['moved']: pre['before migrating: ' + str(prevrow.get(b))] += 1
            if f['ended']: pre[f"before {f['act'][0]}: " + str(prevrow.get(b))] += 1
            if f['restless']: tot['restless & starving' if f['hungry'] >= STARVING else 'restless & not starving'] += 1
            last[b] = w; prevrow[b] = w
    pct = lambda c: ' '.join(f'{k}={100*v/sum(c.values()):.1f}%' for k, v in sorted(c.items(), key=lambda kv: str(kv[0])))
    print(f'[{var}] calm: {pct(calm)}')
    print(f'[{var}] drought: {pct(dro)}')
    print(f'[{var}] calm flicker: {flips/bandyrs:.2f} word changes per band-year')
    print(f'[{var}] ' + ' | '.join(f'{k} x{v}' for k, v in sorted(pre.items())))
    print(f'[{var}] ' + str(dict(tot)))
