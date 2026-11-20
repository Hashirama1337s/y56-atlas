import re,sys
import os
L=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..","lean")+"/"
Q=re.compile(r"q \(?(-?\d+)\)? \(?(-?\d+)\)?")
def prop(a,b):
    # a,b lists of (x,y) meaning x+y*r ; proportional over Q(sqrt2): a_i b_j == a_j b_i
    def mul(p,q): return (p[0]*q[0]+2*p[1]*q[1], p[0]*q[1]+p[1]*q[0])
    return all(mul(a[i],b[j])==mul(a[j],b[i]) for i in range(4) for j in range(4))
t6=open(L+"Y56_L6.lean",encoding="utf-8").read()
def block(t,name):
    i=t.index("def "+name); j=t.index("]]",i); return t[i:j+2]
PN=[[(int(a),int(b)) for a,b in Q.findall(r)] for r in re.findall(r"\[([^\[\]]*)\]",block(t6,"PN"))]
PCN=[[(int(a),int(b)) for a,b in Q.findall(r)] for r in re.findall(r"\[([^\[\]]*)\]",block(t6,"PCN"))]
PL=eval(re.search(r"def PL : [^=]*:= (\[.*\])",t6).group(1))
res={"P2":[],"P4":[],"PC":[]}
for f in ["Y56_L5a","Y56_L5b","Y56_L5c"]:
    t=open(L+f+".lean",encoding="utf-8").read()
    for m in re.finditer(r"/-- (P2|P4|PC) plane #(\d+), normal \[([^\]]*)\](?:, lines \[([^\]]*)\])?",t):
        res[m.group(1)].append((int(m.group(2)),[(int(a),int(b)) for a,b in Q.findall(m.group(3))],m.group(4)))
print({k:len(v) for k,v in res.items()})
bad=[]
for k,off in (("P2",0),("P4",148)):
    for n,nv,ls in res[k]:
        if not prop(nv,PN[off+n]): bad.append((k,n,"normal"))
        if ls is not None and sorted(eval("["+ls+"]"))!=sorted(PL[off+n]): bad.append((k,n,"lines"))
for n,nv,_ in res["PC"]:
    if not prop(nv,PCN[n]): bad.append(("PC",n,"normal"))
print("L5 plane normals/lines vs L6 PN/PL/PCN mismatches:",bad)
