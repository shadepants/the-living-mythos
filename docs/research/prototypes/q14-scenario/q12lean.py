# Q12 probe, step 5: emitter with (a) climate lookback: forage_failed cites drought_began if the band's camp was
# inside the drought at any season in [t - WIN, t]; (b) episode-scoped citations; (c) died_out outcome 'dwindled'
# when perished with no current hunger. Payload facts (stock %, share %) instead of a reason threshold.
# args: WIN pkl...   Throwaway; never port.
import sys, pickle, collections
WIN = int(sys.argv[1]); STABLE = 2
def emit(d):
    ev = []
    def add(t, typ, band, causes, **pl):
        ev.append(dict(id=len(ev), t=t, type=typ, band=band, causes=[c for c in causes if c is not None][:3], pl=pl)); return len(ev)-1
    dr = None
    rows = collections.defaultdict(list)
    for r in d['rows']: rows[r['t']].append(r)
    wt = dict(d['world'])
    st = collections.defaultdict(lambda: dict(nonneg=STABLE, ff=None, open=False, hb=None, sv=None, ph=0, lastin=-10**9))
    for t in sorted(rows):
        for typ in ('drought_began', 'drought_ended'):
            if wt.get(t) == typ or any(w == (t, typ) for w in d['world']):
                x = add(t, typ, 'ROOT', ['CMD'] if typ == 'drought_began' else [dr]); dr = x if typ == 'drought_began' else dr
        for r in sorted(rows[t], key=lambda r: r['band']):
            if r.get('born'): continue
            s = st[r['band']]; b = r['band']
            if r['indrought'] > 0: s['lastin'] = t
            if r['bal'] < 0 and s['nonneg'] >= STABLE:
                c = [dr] if (dr is not None and t - s['lastin'] <= WIN) else []
                s['ff'] = add(t, 'forage_failed', b, c, stockPct=round(100*r['pratio']), sharePct=round(100*r['share'])); s['open'] = True
            s['nonneg'] = s['nonneg']+1 if r['bal'] >= 0 else 0
            if s['nonneg'] >= STABLE and r['hungry'] == 0: s['open'] = False
            ff = s['ff'] if s['open'] else None
            if r['hungry'] >= 1 and s['ph'] == 0: s['hb'] = add(t, 'band_hunger_began', b, [ff]); s['sv'] = None
            if r['hungry'] >= 2 and s['ph'] < 2: s['sv'] = add(t, 'band_starving', b, [s['hb'], ff])
            hung = (s['sv'] or s['hb']) if r['hungry'] > 0 else None
            s['ph'] = r['hungry']; a = r['act']
            if a and a[0] == 'migrated': add(t, 'band_migrated', b, [hung, ff], frm=a[1], to=a[2])
            if a and a[0] in ('dissolved', 'perished'):
                oc = 'dwindled' if (a[0] == 'perished' and hung is None) else a[0]
                add(t, 'band_died_out', b, [hung, ff] if hung else [], outcome=oc, host=a[1] if a[0] == 'dissolved' else None)
            if 'split' in a: add(t, 'band_split', b, [], daughter=a[a.index('split')+1])
    return ev
def hops(ev, eid, tgt):
    fr, seen, h = [eid], {eid}, 0
    while fr and h <= 6:
        if tgt in fr: return h
        nx = []
        for x in fr:
            for c in ev[x]['causes']:
                if isinstance(c, int) and c not in seen: seen.add(c); nx.append(c)
        fr, h = nx, h+1
    return None
tot = collections.Counter()
for p in sys.argv[2:]:
    d = pickle.load(open(p, 'rb')); ev = emit(d); burn = d['burn']
    dr = next(e['id'] for e in ev if e['type'] == 'drought_began')
    win = [e for e in ev if burn <= e['t'] < burn+240]; calm = [e for e in ev if burn-800 <= e['t'] < burn]
    ffw = [e for e in win if e['type'] == 'forage_failed']
    tot['ff drought-window'] += len(ffw); tot['ff drought-window causeless'] += sum(not e['causes'] for e in ffw)
    tot['ff calm'] += sum(e['type'] == 'forage_failed' for e in calm)
    tot['ff cites drought after +40 seasons'] += sum(1 for e in ffw if e['causes'] and e['t']-burn > 40)
    tot['hunger without forage_failed'] += sum(1 for e in ev if e['type'] == 'band_hunger_began' and not e['causes'])
    for e in win:
        if e['type'] in ('band_migrated', 'band_died_out'):
            h = hops(ev, e['id'], dr); k = e['type'] + ('/'+e['pl']['outcome'] if 'outcome' in e['pl'] else '')
            tot[k] += 1; tot[k+(' <=3 hops' if h is not None and h <= 3 else ' NO chain')] += 1
    for e in calm:
        if e['type'] == 'band_died_out': tot['calm died_out/'+e['pl']['outcome']] += 1
for k in sorted(tot): print(f'WIN={WIN}  {k}: {tot[k]}')
