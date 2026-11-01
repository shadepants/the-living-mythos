# Q12 probe, step 4: classify causeless forage_failed events (who, when, migrant?, arrivals nearby, stock ratio, share).
import sys, pickle
sys.argv = ['x', 'spec'] ; import q12emit as E
SP = '/tmp/claude-0/-home-claude/ec322def-7b23-57c0-bcca-31bc1c3cc1bc/scratchpad/'
for f in ['m1_1.5', 'm2_0.9', 'm2_1.5', 'm3_0.9', 'm3_1.5']:
    d = pickle.load(open(SP+f+'.pkl', 'rb')); ev = E.emit(d); burn = d['burn']
    migs = [(e['t'], e['band'], e['pl']['to']) for e in ev if e['type'] == 'band_migrated']
    for e in ev:
        if e['type'] != 'forage_failed' or e['causes']: continue
        r = next(r for r in d['rows'] if r['band'] == e['band'] and r['t'] == e['t'] and not r.get('born'))
        own = [m for m in migs if m[1] == e['band'] and m[0] < e['t']]
        near = [(m[0]-burn, m[1]) for m in migs if m[1] != e['band'] and 0 < e['t']-m[0] <= 16 and (m[2][0]-r['camp'][0])**2+(m[2][1]-r['camp'][1])**2 < 36]
        nxt = [x['type'] for x in ev if x['band'] == e['band'] and e['t'] < x['t'] <= e['t']+16 and x['type'].startswith('band_')]
        print(f, f"t{e['t']-burn:+d}", e['band'], 'migrant before' if own else 'resident', 'arrivals<16s nearby', near,
              'pratio', round(r['pratio'], 2), 'share', round(r['share'], 2), 'next', nxt)
