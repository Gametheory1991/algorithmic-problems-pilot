"""
Pre-registered quick win: Bin packing - First-Fit Decreasing (FFD) vs exact optimum
Clearance-safe: synthetic data only, seed fixed before running. No external data.
Spec (fixed before run): capacity=100, n=12 items, items uniform int 15-60,
200 instances, seeds 0..199 (random.Random(seed)).
Exact optimum: subset DP over all 2^n subsets (feasible = sum <= capacity),
min bins = min partition into feasible subsets. Independent check: validate
both packings (every item used exactly once, no bin over capacity).
"""
import random, json, itertools

CAP=100; N=12; TRIALS=200

def ffd(items):
    bins=[]
    for x in sorted(items, reverse=True):
        placed=False
        for b in bins:
            if sum(b)+x<=CAP:
                b.append(x); placed=True; break
        if not placed: bins.append([x])
    return bins

def optimal(items):
    n=len(items)
    feasible={}
    for mask in range(1,1<<n):
        s=sum(items[i] for i in range(n) if mask>>i & 1)
        if s<=CAP: feasible[mask]=s
    INF=10**9
    dp=[INF]*(1<<n); dp[0]=0; choice=[None]*(1<<n)
    for mask in range(1<<n):
        if dp[mask]==INF: continue
        rem=((1<<n)-1)^mask
        sub=rem
        while sub:
            if sub in feasible:
                nm=mask|sub
                if dp[mask]+1<dp[nm]: dp[nm]=dp[mask]+1; choice[nm]=sub
            sub=(sub-1)&rem
    full=(1<<n)-1
    bins=[]; m=full
    while m:
        sub=choice[m]; bins.append([items[i] for i in range(n) if sub>>i & 1]); m^=sub
    return bins

def valid(packing, items):
    flat=[x for b in packing for x in b]
    return sorted(flat)==sorted(items) and all(sum(b)<=CAP for b in packing)

gaps=[]; worst=None
for seed in range(TRIALS):
    rng=random.Random(seed)
    items=[rng.randint(15,60) for _ in range(N)]
    f=ffd(items); o=optimal(items)
    assert valid(f,items) and valid(o,items), seed
    gap=len(f)-len(o)
    gaps.append(gap)
    if worst is None or gap>worst['gap']:
        worst={'seed':seed,'items':items,'gap':gap,'ffd_bins':len(f),'opt_bins':len(o),'ffd':f,'opt':o}
res={'trials':TRIALS,'instances_ffd_worse':sum(1 for g in gaps if g>0),'max_gap':max(gaps),'mean_gap':sum(gaps)/len(gaps),'worst':worst}
print(json.dumps(res,indent=2))
with open('result.json','w') as fh: json.dump(res,fh,indent=2)
