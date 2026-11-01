# Q16 probe: band-card food-trend variants applied offline to dumped streams (q13run.py pickles).
# args: pkl...   Prints per variant: label shares (calm 200 yr before drought / drought + 20 seasons),
# flicker per band-year, and for bands that go hungry in the drought window: seasons of lead
# between the first 'worsening' label and hunger onset; share reading 'easing' 8 seasons after the drought.
# Throwaway; never port.
import sys, pickle, collections

def press(r):
    # food pressure: effort while fed (0-1), 1 + shortfall once consumption isn't met (continuous through hunger)
    return r['eff'] + r['short']

VARIANTS = {
    # name: (series fn, lag/window, band, kind)
    'bal4 (v0.24)': ('bal', 4, 0.05, 'mean'),
    'effD4 0.05':   ('eff', 4, 0.05, 'delta'),
    'pressD4 0.05': ('press', 4, 0.05, 'delta'),
    'pressD4 0.10': ('press', 4, 0.10, 'delta'),
    'pressMM 0.05': ('press', 4, 0.05, 'meanmean'),
}

def label(hist, kind, lag, band):
    if kind == 'mean':
        h = hist[-lag:]; v = sum(h)/len(h)   # balances already / consumption in the dump
        return 'easing' if v > band else 'worsening' if v < -band else 'steady'
    if kind == 'delta':
        if len(hist) <= lag: return 'steady'
        v = hist[-1] - hist[-1-lag]
    else:  # mean of last lag vs previous lag
        if len(hist) < 2*lag: return 'steady'
        v = sum(hist[-lag:])/lag - sum(hist[-2*lag:-lag])/lag
    # pressure/effort: a fall means food got easier
    return 'easing' if v < -band else 'worsening' if v > band else 'steady'

for name, (ser, lag, band, kind) in VARIANTS.items():
    calm = collections.Counter(); dro = collections.Counter(); flips = 0; byrs = 0.0
    leads = []; after = collections.Counter(); hungry_no_warn = 0
    for p in sys.argv[1:]:
        d = pickle.load(open(p, 'rb')); burn, dur = d['burn'], d['dur']
        hist = collections.defaultdict(list); last = {}; first_worse = {}; onset = {}
        for r in sorted(d['rows'], key=lambda r: (r['t'], r['band'])):
            if r.get('born') or not r.get('cons'): continue
            b, t = r['band'], r['t']
            x = r['bal'] if ser == 'bal' else r['eff'] if ser == 'eff' else press(r)
            hist[b].append(x); hist[b][:] = hist[b][-16:]
            w = label(hist[b], kind, lag, band)
            if burn - 800 <= t < burn:
                calm[w] += 1; byrs += 0.25
                if b in last and last[b] != w: flips += 1
            if burn <= t < burn + dur + 20:
                dro[w] += 1
                if w == 'worsening' and b not in first_worse: first_worse[b] = t
                if r['hungry'] >= 1 and b not in onset: onset[b] = t
            if t == burn + dur + 8: after[w] += 1
            last[b] = w
        for b, t0 in onset.items():
            if b in first_worse and first_worse[b] <= t0: leads.append(t0 - first_worse[b])
            else: hungry_no_warn += 1
    pc = lambda c: ' '.join(f'{k}={100*v/max(1,sum(c.values())):.1f}%' for k, v in sorted(c.items()))
    print(f'[{name}] calm: {pc(calm)} | flicker {flips/max(byrs,1):.2f}/band-yr')
    print(f'[{name}] drought+20: {pc(dro)} | +8 after end: {pc(after)}')
    ls = sorted(leads)
    print(f'[{name}] hunger onsets warned: {len(leads)}/{len(leads)+hungry_no_warn}; lead seasons min/median/max '
          f'{ls[0] if ls else "-"}/{ls[len(ls)//2] if ls else "-"}/{ls[-1] if ls else "-"}')
