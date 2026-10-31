# Q7 model (rev 22) lumped per-cell, from q7b with mDens=0.1
P = dict(rV=0.7, dieBack=0.5, gMax=1.0, halfSat=0.3, need=1.0, maxGraze=0.5,
         condRate=0.6, rMax=0.06, cBreed=0.5, mBase=0.02, mStarve=0.25, cStarve=0.4, n=4, mDens=0.1)
def mf(a): return max(0.2, min(1.2, 1 + 0.8*a))
def eco(V, F, c, Kveg, a, p=P):
    K = Kveg*mf(a)
    V = V + p['rV']*V*(1-V/K) if V <= K else K + (V-K)*(1-p['dieBack'])
    h = 1/p['n']
    for _ in range(p['n']):
        if F <= 0: break
        demand = F*p['gMax']*V/(V+p['halfSat'])*h
        rem = min(demand, p['maxGraze']*h*V)
        sat = min(1.0, rem/(F*p['need']*h))
        c += p['condRate']*h*(sat-c)
        b = p['rMax']*max(0,(c-p['cBreed'])/(1-p['cBreed']))*F*h
        d = (p['mBase'] + p['mDens']*F + p['mStarve']*max(0,(p['cStarve']-c)/p['cStarve']))*F*h
        F += b-d; V -= rem
    return max(V,0), max(F,0), c
if __name__=="__main__":
    for K in (1,2,4):
        V,F,c=K,0.1,0.8
        for t in range(2000): V,F,c=eco(V,F,c,K,0)
        print(K, round(V,3), round(F,3), round(c,3))
