# Q14 probe: pass check and pass-sentence rendering on dumped streams (q13run.py / q14run.py), using the
# rev 36 emitter (q12lean.emit, causeWindow 8). Per run: band outcomes inside the test window
# [drought start, drought end + causeWindow], hops to drought_began, pass = >= 1 band_migrated and >= 1
# non-dwindled band_died_out, each <= 3 hops. Same counts in an equal-length calm window before the drought,
# and for no-drought controls (mag 0). Renders Legends sentences from the real chain. Throwaway; never port.
# args: pkl...
import sys, pickle, collections
sys.argv, files = [sys.argv[0], '8'], sys.argv[1:]
import q12lean
WIN = 8
SEASON = ['spring', 'summer', 'autumn', 'winter']
NAMES = ['Ash', 'Reed', 'Flint', 'Heron', 'Sedge', 'Ochre', 'Thorn', 'Otter', 'Birch', 'Wren', 'Marrow', 'Sloe',
         'Kestrel', 'Bramble', 'Hazel', 'Ember', 'Moss', 'Tern', 'Alder', 'Lark', 'Quill', 'Rowan', 'Sorrel', 'Vole']
names = {}
def nm(b):
    if b not in names: names[b] = NAMES[len(names) % len(NAMES)] + ('' if len(names) < len(NAMES) else str(len(names)//len(NAMES)))
    return names[b]
def when(t): return f'the {SEASON[t % 4]} of year {t // 4}'
def chain(ev, eid):
    out, e = [], ev[eid]
    while True:
        out.append(e)
        nxt = [c for c in e['causes'] if isinstance(c, int)]
        if not nxt: return out
        # follow the forage_failed / climate branch (last cause), which is the 'why' spine
        e = ev[sorted(nxt, key=lambda c: (ev[c]['type'] != 'forage_failed', ev[c]['type'] != 'drought_began'))[0]]

def render(ev, e, dr_t):
    ch = chain(ev, e['id']); ff = next((c for c in ch if c['type'] == 'forage_failed'), None)
    hb = [ev[c] for c in e['causes'] if isinstance(c, int) and ev[c]['type'] in ('band_starving', 'band_hunger_began')]
    hunger = (f"; hunger began in {when(hb[0]['t'])}" if hb else '')
    why = (f"Why? The drought that began in {when(dr_t)} cut its foraging grounds to {ff['pl']['stockPct']}% of their usual yield{hunger}."
           if ff and ff['causes'] else 'Why? (no cause recorded)')
    if e['type'] == 'band_migrated':
        (fx, fy), (tx, ty) = e['pl']['frm'], e['pl']['to']
        d = ((fx-tx)**2 + (fy-ty)**2) ** 0.5
        head = f"The {nm(e['band'])} band left its lands in {when(e['t'])} and walked {round(d*3)} km to new ground."
    else:
        oc = e['pl']['outcome']
        head = (f"The {nm(e['band'])} band broke up in {when(e['t'])}; its last people joined the {nm(e['pl']['host'])} band."
                if oc == 'dissolved' else f"The {nm(e['band'])} band perished in {when(e['t'])}.")
        if oc == 'dissolved': why = why[:-1] + ', and no better land lay within reach.'
    return head + ' ' + why, [c['type'] for c in ch]

tot = collections.Counter()
for p in files:
    d = pickle.load(open(p, 'rb'))
    base = all('pbase' in r for r in d['rows'] if not r.get('born'))
    if base:   # stockPct against base (worldgen) capacity, not the drought-lowered capacity
        for r in d['rows']:
            if not r.get('born'): r['pratio'] = r['pbase']
    ev = q12lean.emit(d); burn, dur = d['burn'], d['dur']
    drs = [e for e in ev if e['type'] == 'drought_began']; dr = drs[0]['id'] if drs else None
    lo, hi = burn, burn + dur + WIN
    def outcomes(a, b):
        res = collections.Counter(); ok = collections.Counter(); first = {}
        for e in ev:
            if a <= e['t'] <= b and e['type'] in ('band_migrated', 'band_died_out'):
                k = e['type'] if e['type'] == 'band_migrated' else 'died_out/' + e['pl']['outcome']
                res[k] += 1
                h = q12lean.hops(ev, e['id'], dr) if dr is not None else None
                if h is not None and h <= 3:
                    ok[k] += 1; first.setdefault(k, e)
        return res, ok, first
    res, ok, first = outcomes(lo, hi)
    calm, _, _ = outcomes(lo - (hi - lo) - 200, lo - 200)
    died = [k for k in ok if k.startswith('died_out/') and k != 'died_out/dwindled']
    passed = ok['band_migrated'] > 0 and bool(died)
    tag = f"{d['scen']} s{d['seed']} m{d['mag']}" + (' [stock vs base K]' if base else ' [stock vs drought K]')
    print(f"{tag}: bands alive {d['nbands']}; window {dict(res)} chained {dict(ok)}; calm window {dict(calm)}; PASS={passed}")
    tot['runs'] += 1; tot['pass'] += passed
    if passed:
        for k in ['band_migrated'] + died[:1]:
            s, c = render(ev, first[k], ev[dr]['t']); print('   ', s); print('      chain:', ' <- '.join(c))
print(dict(tot))
