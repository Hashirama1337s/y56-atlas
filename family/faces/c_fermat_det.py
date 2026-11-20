# Task C follow-up (NUMERICAL): orientation question.  (i) for the h in Aut(F0) with h g02 conj(h)^-1 ~ g' (g' in class of g24),
# the induced real projective map between the real coordinate systems: sign of det.  (ii) whether each sister real
# quartic has a real projective symmetry with det < 0 (then mirror images are projectively equal and orientation is moot).
import sys, pickle, numpy as np
sys.path.insert(0, '../../core/code/sisters')
exec(open('c_fermat.py').read().split("reps = [d['rep']")[0])   # reuse aut, G, S_all, T, proj_eq
gen = {}
for k in ('g12_g13', 'g01_g02_g24_g00'):
    gen.update(pickle.load(open('b_gen_%s.pkl' % k, 'rb')))
Ae = {k: np.array(v['A'].evalf(30).tolist(), dtype=complex) for k, v in gen.items()}
def realise(L):
    k = np.unravel_index(np.argmax(abs(L)), L.shape); L = L/(L[k]/abs(L[k]))
    return L.real if np.abs(L.imag).max() < 1e-8*np.abs(L).max() else None
syms = load_syms()
cent = lambda g: [nm for nm, c, M, _ in syms if np.allclose(S_all[nm] @ G[g], G[g] @ S_all[nm])]
for g in ['g00', 'g01', 'g02', 'g12', 'g13', 'g24']:
    dets = set()
    for nm in cent(g):
        L = realise(np.linalg.inv(Ae[g]) @ S_all[nm] @ Ae[g])
        if L is not None: dets.add(int(np.sign(np.linalg.det(L))))
    print(f'{g}: centraliser order {len(cent(g))}; signs of det of its real symmetries (in sister coords): {sorted(dets)}')
# h with h g02 conj(h)^-1 ~ g24 exactly (g24 class has one member)
signs = set(); n = 0
for h in aut:
    if proj_eq(h @ G['g02'] @ np.linalg.inv(h.conj()), G['g24']):
        L = realise(np.linalg.inv(Ae['g24']) @ h @ Ae['g02'])
        if L is not None: signs.add(int(np.sign(np.linalg.det(L)))); n += 1
print(f'h in Aut(F0) carrying sigma_g02 to sigma_g24: {n}; induced real maps (sister coords) det signs: {sorted(signs)}')
