# Q12 probe, step 2: apply emitter rule variants to dumped streams (q12run.py) and measure
# cause chains. args: variant pkl [pkl ...]   variant: spec | lean
# spec = §14 as written (stableSeasons 2, most-recent forage_failed, climate-only cause).
# lean = episode-scoped causes + reason codes + crowding cause with root shortcut + dwindled outcome.
# Throwaway; never port.
import sys, pickle, collections
VAR = sys.argv[1]
STABLE = 2           # stableSeasons [P]
CROWD_WINDOW = 8     # seasons an arrival counts as a crowding cause
DEPLETED = 0.5       # plant stock / capacity below this at failure -> reason 'depleted' (prototype probe value)

def emit(d):
    ev = []          # dict(id, t, type, band, causes, payload)
    def add(t, typ, band, causes, **pl):
        e = dict(id=len(ev), t=t, type=typ, band=band, causes=[c for c in causes if c is not None][:3], pl=pl); ev.append(e); return e['id']
    roots = {}
    for t, typ in d['world']:
        roots[typ] = add(t, typ, 'ROOT', [roots.get('drought_began')] if typ == 'drought_ended' else ['CMD'])
    drought = roots.get('drought_began')
    by_t = collections.defaultdict(list)
    for r in d['rows']: by_t[r['t']].append(r)
    st = collections.defaultdict(lambda: dict(nonneg=STABLE, ff=None, ffopen=False, hb=None, sv=None, prevh=0))
    last_arrival = []   # (t, camp, event id, root cause of that arrival)
    def rootof(eid):
        # climate root reachable from eid through forage_failed causes (for the crowding shortcut)
        seen = [eid]
        while seen:
            x = seen.pop()
            if x == drought: return drought
            if isinstance(x, int): seen += [c for c in ev[x]['causes'] if isinstance(c, int)]
        return None
    for t in sorted(by_t):
        for r in sorted(by_t[t], key=lambda r: r['band']):   # band order (names stand in for IDs)
            s = st[r['band']]; b = r['band']
            if r.get('born'):
                continue
            # forage_failed
            if r['bal'] < 0 and s['nonneg'] >= STABLE:
                causes = []; reason = 'unknown'
                if r['indrought'] > 0 and drought is not None: causes.append(drought); reason = 'drought'
                if VAR == 'lean':
                    near = [a for a in last_arrival if t - a[0] <= CROWD_WINDOW and a[3] != b and a[1] is not None and
                            ((a[1][0]-r['camp'][0])**2 + (a[1][1]-r['camp'][1])**2) < (2*3)**2]
                    if near:
                        a = near[-1]; causes.append(a[2])
                        if a[4] is not None and a[4] not in causes: causes.append(a[4])   # root shortcut
                        if reason == 'unknown': reason = 'crowded'
                    if reason == 'unknown': reason = 'depleted' if r['pratio'] < DEPLETED else 'shortfall'
                s['ff'] = add(t, 'forage_failed', b, causes, reason=reason, pratio=round(r['pratio'], 2), share=round(r['share'], 2))
                s['ffopen'] = True
            s['nonneg'] = s['nonneg'] + 1 if r['bal'] >= 0 else 0
            if VAR == 'lean' and s['nonneg'] >= STABLE and r['hungry'] == 0: s['ffopen'] = False   # episode closes
            ff = s['ff'] if (VAR == 'spec' or s['ffopen']) else None
            # hunger
            if r['hungry'] >= 1 and s['prevh'] == 0: s['hb'] = add(t, 'band_hunger_began', b, [ff]); s['sv'] = None
            if r['hungry'] >= 2 and s['prevh'] < 2: s['sv'] = add(t, 'band_starving', b, [s['hb'], ff])
            if r['hungry'] == 0: hb = sv = None
            else: hb, sv = s['hb'], s['sv']
            s['prevh'] = r['hungry']
            act = r['act']
            if act and act[0] == 'migrated':
                e = add(t, 'band_migrated', b, [sv or hb, ff], frm=act[1], to=act[2])
                last_arrival.append((t, act[2], e, b, rootof(e)))
            if act and act[0] in ('dissolved', 'perished'):
                hunger = sv or hb
                if VAR == 'lean' and hunger is None:
                    outcome = 'dwindled' if act[0] == 'perished' else 'dissolved'
                else: outcome = act[0]
                add(t, 'band_died_out', b, [hunger, ff] if hunger else ([ff] if VAR == 'spec' else []),
                    outcome=outcome, host=act[1] if act[0] == 'dissolved' else None, pop0=r['pop0'],
                    hungry=r['hungry'])
            if 'split' in act:
                i = act.index('split'); e = add(t, 'band_split', b, [], daughter=act[i+1])
                last_arrival.append((t, None, e, b, None))
    # fix split arrivals: daughter camp is unknown here; drop them from crowding (camp None)
    return ev

def hops(ev, eid, target):
    if target is None: return None
    frontier, seen, h = [eid], {eid}, 0
    while frontier and h <= 6:
        if target in frontier: return h
        nxt = []
        for x in frontier:
            for c in ev[x]['causes']:
                if isinstance(c, int) and c not in seen: seen.add(c); nxt.append(c)
        frontier, h = nxt, h+1
    return None

def report(path):
    d = pickle.load(open(path, 'rb')); ev = emit(d); burn = d['burn']
    drought = next((e['id'] for e in ev if e['type'] == 'drought_began'), None)
    calm = [e for e in ev if burn-800 <= e['t'] < burn]
    dro = [e for e in ev if burn <= e['t'] < burn+240]
    cnt = lambda es: collections.Counter(e['type'] for e in es)
    out = [f"{d['scen']} s{d['seed']} m{d['mag']} dens {' '.join(f'{x:.2f}' for x in d['dens'])}"]
    out.append('  calm 200yr: ' + ' '.join(f'{k}={v}' for k, v in sorted(cnt(calm).items())))
    out.append('  drought 60yr: ' + ' '.join(f'{k}={v}' for k, v in sorted(cnt(dro).items())))
    ffr = collections.Counter(e['pl'].get('reason') for e in calm if e['type'] == 'forage_failed')
    out.append('  calm forage_failed reasons: ' + str(dict(ffr)))
    for e in [e for e in ev if e['type'] in ('band_migrated', 'band_died_out') and e['t'] >= burn-800]:
        h = hops(ev, e['id'], drought) if e['t'] >= burn else None
        exposed = any(r['band'] == e['band'] and burn <= r['t'] < burn+d['dur'] and r.get('indrought', 0) > 0 for r in d['rows'])
        ffc = [ev[c] for c in e['causes'] if isinstance(c, int) and ev[c]['type'] == 'forage_failed']
        age = e['t'] - ffc[0]['t'] if ffc else None
        reason = ffc[0]['pl'].get('reason') if ffc else None
        out.append(f"  t{e['t']-burn:+5d} {e['type']:14s} {e['band']:12s} {str(e['pl'].get('outcome','')):9s} causes={[ev[c]['type'][:12] if isinstance(c,int) else c for c in e['causes']]} "
                   f"hops={h} exposed={exposed} ffage={age} reason={reason} hungry={e['pl'].get('hungry','')} pop0={e['pl'].get('pop0','')}")
    return '\n'.join(out)

for p in sys.argv[2:]: print(report(p))
