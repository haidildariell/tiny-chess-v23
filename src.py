import json,os,sys,random,urllib.request,urllib.error
ENV=os.environ.get("MAKEFUN_ENV_URL") or sys.exit("no env")
BG=150000
INF=10**9
MATE=100000
V=(0,100,320,330,500,900,0)
PS="KKKKKKKKLLLLLLLLLLMMMMLLMMNOONMMNNOPPONNOOPRRPOOSSSSSSSSKKKKKKKKEGIIIIGEGIKKKKIGIKMNNMKIILNOONLIIKNOONKIILMNNMLIGIKLLKIGEGIIIIGEGIIIIIIGIKKKKKKIIKLMMLKIILLMMLLIIKMMMMKIIMMMMMMIILKKKKLIGIIIIIIGKKKKKKKKLMMMMMMLJKKKKKKJJKKKKKKJJKKKKKKJJKKKKKKJJKKKKKKJKKKLLKKKGIIJJIIGIKKKKKKIIKLLLLKIJKLLLLKJKKLLLLKJILLLLLKIIKLKKKKIGIIJJIIGECCAACCEECCAACCEECCAACCEECCAACCEGEECCEEGIGGGGGGIOOKKKKOOOQMKKMQO"
PST=tuple((ord(c)-75)*5 for c in PS)
R=random.Random(987654321)
ZB=[[R.getrandbits(64) for _ in range(128)] for _ in range(12)]
ZS=R.getrandbits(64)
ZC=[R.getrandbits(64) for _ in range(16)]
ZE=[R.getrandbits(64) for _ in range(8)]
PX=[(s>>4)*8+(s&7) for s in range(128)]
CK=[15]*128
for i,v in ((0,13),(7,14),(4,12),(112,7),(119,11),(116,3)):CK[i]=v
ND=(33,31,18,14,-14,-18,-31,-33)
KD=(1,-1,16,-16,15,17,-15,-17)
BD=(15,17,-15,-17)
RD=(1,-1,16,-16)
CT=((0,1,(5,6),(4,5,6),4,6),(0,2,(1,2,3),(4,3,2),4,2),(1,4,(117,118),(116,117,118),116,118),(1,8,(113,114,115),(116,115,114),116,114))
B=[0]*128
L=[[],[]]
IX=[0]*128
KS=[4,116]
SD=0
CA=0
EP=-1
HM=0
K=0
ST=[]
HIST=set()
TT={}
KL=[[0,0] for _ in range(256)]
HH=[0]*131072
N=[0]
class X(Exception):pass
def tick():
    N[0]+=1
    if N[0]&255==0 and N[0]>BG:raise X
def zi(p):return p-1 if p>0 else 5-p
def setup(fen):
    global SD,CA,EP,HM,K
    fp=fen.split()
    B[:]=[0]*128
    L[0][:]=[]
    L[1][:]=[]
    ST[:]=[]
    K=0
    sq=112
    for c in fp[0]:
        if c=="/":sq-=24
        elif c.isdigit():sq+=int(c)
        else:
            p="PNBRQK".index(c.upper())+1
            if c.islower():p=-p
            B[sq]=p
            c0=0 if p>0 else 1
            IX[sq]=len(L[c0])
            L[c0].append(sq)
            if abs(p)==6:KS[c0]=sq
            K^=ZB[zi(p)][sq]
            sq+=1
    SD=0 if fp[1]=="w" else 1
    CA=0
    if fp[2]!="-":
        for c in fp[2]:CA|=1<<"KQkq".index(c)
    EP=-1 if fp[3]=="-" else (ord(fp[3][0])-97)+(int(fp[3][1])-1)*16
    HM=int(fp[4])
    if SD:K^=ZS
    K^=ZC[CA]
    if EP>=0:K^=ZE[EP&7]
def att(s,c):
    g=1 if c==0 else -1
    for t in (s-15*g,s-17*g):
        if not t&0x88 and B[t]==g:return True
    for o in ND:
        t=s+o
        if not t&0x88 and B[t]==2*g:return True
    for o in KD:
        t=s+o
        if not t&0x88 and B[t]==6*g:return True
    for ds,ps in ((BD,(3,5)),(RD,(4,5))):
        for o in ds:
            t=s+o
            while not t&0x88:
                q=B[t]
                if q:
                    if q*g>0 and abs(q) in ps:return True
                    break
                t+=o
    return False
def gen(cap):
    ms=[]
    sg=1 if SD==0 else -1
    d=16*sg
    lr=7 if SD==0 else 0
    sr=1 if SD==0 else 6
    for f in L[SD]:
        p=B[f]
        a=abs(p)
        if a==1:
            t=f+d
            if not t&0x88 and B[t]==0:
                if (t>>4)==lr:
                    for pr in (5,4,3,2):ms.append(f|t<<7|pr<<14)
                elif not cap:
                    ms.append(f|t<<7)
                    if (f>>4)==sr and B[f+2*d]==0:ms.append(f|(f+2*d)<<7)
            for o in (d-1,d+1):
                t=f+o
                if t&0x88:continue
                q=B[t]
                if (q and q*sg<0) or t==EP:
                    if (t>>4)==lr:
                        for pr in (5,4,3,2):ms.append(f|t<<7|pr<<14)
                    else:ms.append(f|t<<7)
        elif a==2 or a==6:
            for o in ND if a==2 else KD:
                t=f+o
                if t&0x88:continue
                q=B[t]
                if q==0:
                    if not cap:ms.append(f|t<<7)
                elif q*sg<0:ms.append(f|t<<7)
            if a==6 and not cap:
                for sd,bt,es,ks,f0,t0 in CT:
                    if sd==SD and CA&bt and all(B[e]==0 for e in es) and not any(att(k,1-SD) for k in ks):ms.append(f0|t0<<7)
        else:
            ds=BD if a==3 else RD if a==4 else BD+RD
            for o in ds:
                t=f+o
                while not t&0x88:
                    q=B[t]
                    if q==0:
                        if not cap:ms.append(f|t<<7)
                    else:
                        if q*sg<0:ms.append(f|t<<7)
                        break
                    t+=o
    return ms
def drop(sq,c):
    lst=L[c]
    i=IX[sq]
    last=lst[-1]
    lst[i]=last
    IX[last]=i
    lst.pop()
def slide(a,b):
    lst=L[SD]
    i=IX[a]
    lst[i]=b
    IX[b]=i
def make(m):
    global SD,CA,EP,HM,K
    f=m&127
    t=(m>>7)&127
    pr=m>>14
    p=B[f]
    sg=1 if p>0 else -1
    cap=B[t]
    cs=t
    if abs(p)==1 and t==EP and cap==0:
        cs=t-16*sg
        cap=B[cs]
    rf=rt=-1
    if abs(p)==6 and abs(t-f)==2:
        if t>f:rf,rt=t+1,t-1
        else:rf,rt=t-2,t+1
    ST.append((m,cap,cs,CA,EP,HM,rf,rt,K,p))
    K^=ZB[zi(p)][f]
    if cap:
        K^=ZB[zi(cap)][cs]
        drop(cs,1-SD)
        B[cs]=0
    slide(f,t)
    np=sg*pr if pr else p
    B[f]=0
    B[t]=np
    K^=ZB[zi(np)][t]
    if abs(p)==6:KS[SD]=t
    if rf>=0:
        r=B[rf]
        slide(rf,rt)
        B[rf]=0
        B[rt]=r
        K^=ZB[zi(r)][rf]^ZB[zi(r)][rt]
    nca=CA&CK[f]&CK[t]
    if nca!=CA:
        K^=ZC[CA]^ZC[nca]
        CA=nca
    nep=(f+t)//2 if abs(p)==1 and abs(t-f)==32 else -1
    if EP>=0:K^=ZE[EP&7]
    if nep>=0:K^=ZE[nep&7]
    EP=nep
    HM=0 if cap or abs(p)==1 else HM+1
    SD^=1
    K^=ZS
    if att(KS[1-SD],SD):
        unmake()
        return False
    return True
def unmake():
    global SD,CA,EP,HM,K
    m,cap,cs,ca,ep,hm,rf,rt,k,p=ST.pop()
    f=m&127
    t=(m>>7)&127
    SD^=1
    if rf>=0:
        r=B[rt]
        slide(rt,rf)
        B[rt]=0
        B[rf]=r
    slide(t,f)
    B[t]=0
    B[f]=p
    if cap:
        lst=L[1-SD]
        IX[cs]=len(lst)
        lst.append(cs)
        B[cs]=cap
    if abs(p)==6:KS[SD]=f
    CA,EP,HM,K=ca,ep,hm,k
def ev():
    s=0
    bp=[0,0]
    mn=[0,0]
    hv=[0,0]
    for sd in (0,1):
        g=1 if sd==0 else -1
        for q in L[sd]:
            p=B[q]*g
            s+=g*(V[p]+PST[(p-1)*64+(PX[q] if sd==0 else PX[q^112])])
            if p==3:
                bp[sd]+=1
                mn[sd]+=1
            elif p==2:mn[sd]+=1
            elif p<6:hv[sd]+=1
    if not hv[0]+hv[1] and mn[0]+mn[1]<2:return 0
    s+=30*((bp[0]==2)-(bp[1]==2))
    return s if SD==0 else -s
def sc(m):
    t=(m>>7)&127
    v=B[t]
    if v:return (V[abs(v)]<<4)-V[abs(B[m&127])]
    return 1000 if m>>14 else 0
def order(ms,tt,p):
    a,b=KL[p&255]
    def key(m):
        s=sc(m)
        return (1<<20) if m==tt else ((1<<18)+s if s else ((1<<17) if m==a else ((1<<17)-1 if m==b else HH[m])))
    ms.sort(key=key,reverse=True)
def qs(a,b,p):
    tick()
    if p and K in HIST:return 0
    inch=att(KS[SD],1-SD)
    if inch:
        ms=gen(0)
        sp=-INF
    else:
        sp=ev()
        if sp>=b:return sp
        if sp>a:a=sp
        ms=gen(1)
    ms.sort(key=sc,reverse=True)
    played=False
    for m in ms:
        if not inch and not(m>>14):
            t=(m>>7)&127
            if sp+V[abs(B[t])]+200<a:continue
        if not make(m):continue
        played=True
        s=-qs(-b,-a,p+1)
        unmake()
        if s>a:a=s
        if a>=b:break
    if not played:return -MATE+p if inch else a
    return a
def srch(a,b,d,p):
    tick()
    if p and (K in HIST or HM>=100):return 0
    inch=att(KS[SD],1-SD)
    if d>0 and inch:d+=1
    e=TT.get(K)
    tt=0
    if e:
        tt=e[3]
        if e[0]>=d:
            s=e[2]
            if s>90000:s-=p
            elif s<-90000:s+=p
            if e[1]==0:return s
            if e[1]==1 and s>=b:return s
            if e[1]==2 and s<=a:return s
    if d<=0:return qs(a,b,p)
    ms=gen(0)
    order(ms,tt,p)
    best=-INF
    bm=0
    a0=a
    n=0
    for m in ms:
        if not make(m):continue
        n+=1
        if bm:
            if d>=3 and n>3 and not inch and not sc(m):
                s=-srch(-a-1,-a,d-2,p+1)
                if s>a:s=-srch(-b,-a,d-1,p+1)
            else:
                s=-srch(-a-1,-a,d-1,p+1)
                if a<s<b:s=-srch(-b,-a,d-1,p+1)
        else:
            s=-srch(-b,-a,d-1,p+1)
        unmake()
        if s>best:
            best=s
            bm=m
        if s>a:a=s
        if a>=b:
            if not sc(m):
                HH[m]+=d*d
                if KL[p&255][0]!=m:
                    KL[p&255][1]=KL[p&255][0]
                    KL[p&255][0]=m
            break
    if not bm:return -MATE+p if inch else 0
    fl=1 if a>=b else 0 if best>a0 else 2
    s=best
    if s>90000:s+=p
    elif s<-90000:s-=p
    TT[K]=(d,fl,s,bm)
    return best
def sweep(ms,d,a,b):
    cb=ms[0]
    cs=-INF
    al=a
    for i,m in enumerate(ms):
        if not make(m):continue
        if i==0:s=-srch(-b,-al,d-1,1)
        else:
            s=-srch(-al-1,-al,d-1,1)
            if al<s<b:s=-srch(-b,-al,d-1,1)
        unmake()
        if s>cs:
            cs=s
            cb=m
        if s>al:al=s
    return cb,cs
def root():
    ms=gen(0)
    legal=[]
    for m in ms:
        if make(m):
            legal.append(m)
            unmake()
    if not legal:return 0,0
    order(legal,0,0)
    best=legal[0]
    bs=-INF
    N[0]=0
    if len(TT)>200000:TT.clear()
    for d in range(1,64):
        try:
            if d>=5 and -90000<bs<90000:
                cb,cs=sweep(legal,d,bs-40,bs+40)
                if cs<=bs-40 or cs>=bs+40:cb,cs=sweep(legal,d,-INF,INF)
            else:cb,cs=sweep(legal,d,-INF,INF)
            best=cb
            bs=cs
            legal.remove(best)
            legal.insert(0,best)
        except X:break
        if bs>90000 or bs<-90000:break
    return best,bs
def call(path,body):
    req=urllib.request.Request(ENV+path,data=json.dumps(body).encode(),headers={"content-type":"application/json"})
    try:
        with urllib.request.urlopen(req,timeout=30) as r:return json.load(r)
    except urllib.error.HTTPError as e:sys.exit(f"{path}: {e.code} {e.read().decode(errors='replace')}")
def uci(m):
    f=m&127
    t=(m>>7)&127
    s=chr(97+(f&7))+str((f>>4)+1)+chr(97+(t&7))+str((t>>4)+1)
    if m>>14:s+=" pnbrq"[m>>14]
    return s
CG=[0]
def prepare(fen,gid):
    setup(fen)
    if gid!=CG[0]:
        CG[0]=gid
        HIST.clear()
    HIST.add(K)
if __name__=="__main__":
    while True:
        g=call("/game",{})
        if g["status"]=="done":break
        while g["status"]=="your_move":
            prepare(g["fen"],g["game"])
            try:m,s=root()
            except Exception as e:
                print(f"root error: {e!r}",file=sys.stderr)
                m,s=0,0
            u=uci(m) if m else None
            if not u or u not in g["legal_moves"]:u=g["legal_moves"][0]
            print(u,N[0],s,file=sys.stderr)
            g=call("/move",{"game":g["game"],"move":u})
        print(f"game {g['game']}: {g['outcome']} by {g['reason']}",file=sys.stderr)
    print(f"done: {g.get('wins')} won, {g.get('draws')} drawn, {g.get('losses')} lost",file=sys.stderr)
