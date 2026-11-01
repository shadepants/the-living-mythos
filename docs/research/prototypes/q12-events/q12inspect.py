# Q12 probe, step 3: history of causeless perishings; whole-run forage_failed causes; stale citations.
import sys, pickle, collections
sys.argv = ['x', 'spec'] ; import q12emit as E
SP = '/tmp/claude-0/-home-claude/ec322def-7b23-57c0-bcca-31bc1c3cc1bc/scratchpad/'
for f in ['m1_1.5', 'm3_0.9', 'm1_0.9', 'm2_0.9', 'm2_1.5', 'm3_1.5']:
    d = pickle.load(open(SP+f+'.pkl', 'rb')); ev = E.emit(d); burn = d['burn']
    ff = [e for e in ev if e['type'] == 'forage_failed']
    print(f, 'whole run forage_failed', len(ff), 'no cause', sum(1 for e in ff if not e['causes']),
          'by century (no cause):', collections.Counter((e['t']//400) for e in ff if not e['causes']))
    for e in ev:
        if e['type'] == 'band_died_out' and not e['causes']:
            b = e['band']; rs = [r for r in d['rows'] if r['band'] == b and not r.get('born')]
            born = next((r for r in d['rows'] if r['band'] == b and r.get('born')), None)
            print('  dwindled', b, 'founded t', (born['t']-burn) if born else 'start', 'pop at founding', born['pop'] if born else '-',
                  'ended t', e['t']-burn)
            last = rs[-60:]
            print('   pop last 60 seasons:', [int(r['pop']) for r in last][::4])
            print('   hungry seasons in last 60:', sum(1 for r in last if r['hungry'] > 0), 'eff mean', round(sum(r['eff'] for r in last)/len(last), 2),
                  'share mean', round(sum(r['share'] for r in last)/len(last), 2), 'acts', [(r['t']-burn, r['act']) for r in rs if r['act']])
