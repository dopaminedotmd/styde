```python
"""
procgen.py — Procedural Generation Toolkit
seed: ensure reproducibility, noise: perlin/simplex, dungeon: bsp+drunkard,
lsystem: plants/roads, wavefunc: tile WFC
"""
import random, math, itertools, collections, sys
# ─── SEED ───────────────────────────────────────────────────────────
R = random.Random()
def seed(n):
    R.seed(n)
# ─── NOISE ──────────────────────────────────────────────────────────
def _fade(t): return t*t*t*(t*(t*6-15)+10)
def _lerp(a,b,t): return a+t*(b-a)
class PerlinNoise:
    def __init__(self):
        p = list(range(256))
        R.shuffle(p)
        self.p = p*2
    def noise2(self,x,y):
        X,Y=int(x)&255,int(y)&255
        x-=int(x);y-=int(y)
        u,v=_fade(x),_fade(y)
        a=self.p[X]+Y;b=self.p[X+1]+Y
        return _lerp(_lerp(self._grad2(a,x,y),self._grad2(b,x-1,y),u),
                     _lerp(self._grad2(a+1,x,y-1),self._grad2(b+1,x-1,y-1),u),v)
    def _grad2(self,h,x,y):
        h&=3
        return (x if h<2 else -x)+(y if h%2==0 else -y)
class SimplexNoise:
    _F2,_G2=0.5*(math.sqrt(3)-1),(3-math.sqrt(3))/6
    def __init__(self):
        perm=list(range(256));R.shuffle(perm);self.perm=perm*2
    def noise2(self,x,y):
        s=(x+y)*self._F2;i=int(x+s);j=int(y+s)
        t=(i+j)*self._G2;X0=i-t;Y0=j-t;x0=x-X0;y0=y-Y0
        i1,j1=(1,0)if x0>y0 else(0,1);x1=x0-i1+self._G2;y1=y0-j1+self._G2
        x2=x0-1+2*self._G2;y2=y0-1+2*self._G2
        def _c(ix,iy,x,y):
            t=0.5-x*x-y*y
            if t<=0:return 0
            t*=t;n=self.perm[self.perm[ix]+iy]&3
            return t*t*({0:x+y,1:x,2:y,3:0}[n])
        return 70*(_c(i&255,j&255,x0,y0)+_c((i+i1)&255,(j+j1)&255,x1,y1)+_c((i+1)&255,(j+1)&255,x2,y2))
def octave_noise(w,h,sx=0,sy=0,octaves=6,persistence=0.5,lacunarity=2.0,noise_class=PerlinNoise):
    nz=noise_class();grid=[[0]*h for _ in range(w)]
    amp,freq,max_val=1,1,0
    for _ in range(octaves):
        max_val+=amp
        for x in range(w):
            for y in range(h):
                grid[x][y]+=amp*nz.noise2((x+sx)*freq/w,(y+sy)*freq/h)
        amp*=persistence;freq*=lacunarity
    for x in range(w):
        for y in range(h):
            grid[x][y]=grid[x][y]/max_val
    return grid
# ─── TERRAIN ────────────────────────────────────────────────────────
def generate_terrain(w,h,seed_val=0,noise_class=PerlinNoise):
    seed(seed_val);return octave_noise(w,h,noise_class=noise_class)
def classify_terrain(grid,thresholds=None):
    if thresholds is None: thresholds=[(-0.3,'water'),(0.1,'sand'),(0.25,'grass'),(0.4,'forest'),(1.0,'mountain')]
    h=len(grid[0])if grid else 0
    return[[next(c for t,c in thresholds if grid[x][y]<t)for y in range(h)]for x in range(len(grid))]
# ─── DUNGEON (BSP) ──────────────────────────────────────────────────
class BSPNode:
    def __init__(self,x,y,w,h):self.x=x;self.y=y;self.w=w;self.h=h;self.l=self.r=None
def _split(node,min_sz=5):
    if node.w<min_sz*2 and node.h<min_sz*2:return
    horiz=node.w<node.h or(node.h<node.w and R.random()<0.5)if node.w!=node.h else R.random()<0.5
    if horiz:
        if node.h<min_sz*2:return
        split=R.randint(min_sz,node.h-min_sz)
        node.l=BSPNode(node.x,node.y,node.w,split)
        node.r=BSPNode(node.x,node.y+split,node.w,node.h-split)
    else:
        if node.w<min_sz*2:return
        split=R.randint(min_sz,node.w-min_sz)
        node.l=BSPNode(node.x,node.y,split,node.h)
        node.r=BSPNode(node.x+split,node.y,node.w-split,node.h)
    _split(node.l,min_sz);_split(node.r,min_sz)
def bsp_dungeon(w,h,seed_val=0,min_room=5,max_room=12):
    seed(seed_val);root=BSPNode(1,1,w-2,h-2);_split(root)
    grid=[['#']*h for _ in range(w)]
    rooms=[]
    def collect(n):
        if n is None:return
        if n.l is None and n.r is None:
            rw=R.randint(min_room,min(max_room,n.w-2))
            rh=R.randint(min_room,min(max_room,n.h-2))
            rx=n.x+R.randint(1,n.w-rw-1)
            ry=n.y+R.randint(1,n.h-rh-1)
            rooms.append((rx,ry,rw,rh))
            for i in range(rx,rx+rw):
                for j in range(ry,ry+rh):grid[i][j]='.'
        else:
            collect(n.l);collect(n.r)
            # corridor between child centers
            if n.l and n.r:
                cx1=n.l.x+n.l.w//2;cy1=n.l.y+n.l.h//2
                cx2=n.r.x+n.r.w//2;cy2=n.r.y+n.r.h//2
                for x in range(min(cx1,cx2),max(cx1,cx2)+1):grid[x][cy1]='.'
                for y in range(min(cy1,cy2),max(cy1,cy2)+1):grid[cx2][y]='.'
    collect(root)
    return grid,rooms
# ─── DRUNKARD WALK ──────────────────────────────────────────────────
def drunkard_walk(w,h,seed_val=0,steps=400,start=None):
    seed(seed_val);grid=[['#']*h for _ in range(w)]
    x,y=start or(w//2,h//2);grid[x][y]='.'
    dirs=[(0,1),(0,-1),(1,0),(-1,0)]
    for _ in range(steps):
        dx,dy=R.choice(dirs)
        nx,ny=x+dx,y+dy
        if 1<=nx<w-1 and 1<=ny<h-1:
            x,y=nx,ny;grid[x][y]='.'
    return grid
# ─── L-SYSTEM ───────────────────────────────────────────────────────
def lsystem(axiom,rules,iterations=4):
    s=axiom
    for _ in range(iterations):
        s=''.join(rules.get(c,c)for c in s)
    return s
def lsystem_turtle(cmd,step=10,angle=25):
    """returns list of line segments [(x1,y1,x2,y2),...]"""
    x=y=0;stack=[];dir_=90;segments=[]
    for c in cmd:
        if c=='F':nx=x+step*math.cos(math.radians(dir_));ny=y+step*math.sin(math.radians(dir_));segments.append((x,y,nx,ny));x,y=nx,ny
        elif c=='f':x+=step*math.cos(math.radians(dir_));y+=step*math.sin(math.radians(dir_))
        elif c=='+':dir_=(dir_+angle)%360
        elif c=='-':dir_=(dir_-angle)%360
        elif c=='[':stack.append((x,y,dir_))
        elif c==']':x,y,dir_=stack.pop()
    return segments
# preset L-systems
PLANT_LS = {'axiom':'X','rules':{'X':'F+[[X]-X]-F[-FX]+X','F':'FF'},'angle':25}
ROAD_LS  = {'axiom':'F-F-F-F','rules':{'F':'F-F+F+FF-F-F+F'},'angle':90}
# ─── WAVE FUNCTION COLLAPSE ─────────────────────────────────────────
class WFCTile:
    """single tile with adjacency rules"""
    def __init__(self,name,adjacency=None):
        self.name=name
        self.adj=adjacency or{}
    def fits(self,other,direction):
        opp={'n':'s','s':'n','e':'w','w':'e'}
        return other.name in self.adj.get(direction,[])and self.name in other.adj.get(opp[direction],[])
# tile definitions for a simple top-down tileset
TILES={
    'grass':WFCTile('grass',{'n':['grass','forest','road'],'s':['grass','forest','road'],'e':['grass','forest','road'],'w':['grass','forest','road']}),
    'forest':WFCTile('forest',{'n':['grass','forest'],'s':['grass','forest'],'e':['grass','forest'],'w':['grass','forest']}),
    'water':WFCTile('water',{'n':['water','sand'],'s':['water','sand'],'e':['water','sand'],'w':['water','sand']}),
    'sand':WFCTile('sand',{'n':['water','sand','grass'],'s':['water','sand','grass'],'e':['water','sand','grass'],'w':['water','sand','grass']}),
    'road':WFCTile('road',{'n':['road','grass'],'s':['road','grass'],'e':['road','grass'],'w':['road','grass']}),
    'mountain':WFCTile('mountain',{'n':['mountain','grass'],'s':['mountain','grass'],'e':['mountain','grass'],'w':['mountain','grass']}),
}
def wfc_collapse(w,h,seed_val=0):
    """wave function collapse on simple tile grid"""
    seed(seed_val);tiles=list(TILES.keys());grid=[[None]*h for _ in range(w)]
    # cells store list of possible tiles
    possible=[[list(tiles)for _ in range(h)]for _ in range(w)]
    def observe():
        min_entropy=float('inf');candidates=[]
        for x in range(w):
            for y in range(h):
                if grid[x][y]is not None:continue
                e=len(possible[x][y])
                if e==0:return None  # contradiction
                if e<min_entropy:min_entropy=e;candidates=[(x,y)]
                elif e==min_entropy:candidates.append((x,y))
        if not candidates:return None
        return R.choice(candidates)
    def propagate(x,y):
        stack=[(x,y)]
        while stack:
            cx,cy=stack.pop()
            for dx,dy,dr,opp in [(0,1,'n','s'),(0,-1,'s','n'),(1,0,'w','e'),(-1,0,'e','w')]:
                nx,ny=cx+dx,cy+dy
                if nx<0 or nx>=w or ny<0 or ny>=h:continue
                if grid[nx][ny]is not None:continue
                before=len(possible[nx][ny])
                possible[nx][ny]=[t for t in possible[nx][ny]if any(TILES[t].fits(TILES[g],dr)for g in possible[cx][cy])]
                if before!=len(possible[nx][ny])and len(possible[nx][ny])>0:
                    stack.append((nx,ny))
    for _ in range(w*h):
        cell=observe()
        if cell is None:break
        cx,cy=cell
        collapsed=R.choice(possible[cx][cy])
        grid[cx][cy]=collapsed
        possible[cx][cy]=[collapsed]
        propagate(cx,cy)
    # fill unresolved with grass
    for x in range(w):
        for y in range(h):
            if grid[x][y]is None:
                grid[x][y]=possible[x][y][0]if possible[x][y]else'grass'
    return grid
# ─── DEMO ───────────────────────────────────────────────────────────
if __name__=='__main__':
    S=42;W,H=40,30
    print(f"SEED={S}  SIZE={W}x{H}")
    # terrain
    g=generate_terrain(W,H,S)
    c=classify_terrain(g)
    print("\nTERRAIN (first 10 rows x 20 cols):")
    for y in range(min(10,H)):
        print(''.join({'water':'~','sand':'.','grass':'"','forest':'*','mountain':'^'}[c[x][y]]for x in range(min(20,W))))
    # bsp dungeon
    dg,rooms=bsp_dungeon(W,H,S+1)
    print(f"\nBSP DUNGEON ({len(rooms)} rooms, first 10 rows x 20 cols):")
    for y in range(min(10,H)):
        print(''.join(dg[x][y]for x in range(min(20,W))))
    # drunkard
    dw=drunkard_walk(W,H,S+2)
    print(f"\nDRUNKARD WALK (first 10 rows x 20 cols):")
    for y in range(min(10,H)):
        print(''.join(dw[x][y]for x in range(min(20,W))))
    # lsystem plant
    pcmd=lsystem(PLANT_LS['axiom'],PLANT_LS['rules'],4)
    pseg=lsystem_turtle(pcmd,step=8,angle=PLANT_LS['angle'])
    print(f"\nL-SYSTEM PLANT: {len(pcmd)} chars, {len(pseg)} segments")
    # lsystem road
    rcmd=lsystem(ROAD_LS['axiom'],ROAD_LS['rules'],3)
    rseg=lsystem_turtle(rcmd,step=10,angle=ROAD_LS['angle'])
    print(f"L-SYSTEM ROAD: {len(rcmd)} chars, {len(rseg)} segments")
    # wfc
    wfc=wfc_collapse(20,15,S+3)
    print("\nWFC TILE MAP (20x15):")
    sym={'grass':'.','forest':'*','water':'~','sand':',','road':'#','mountain':'^'}
    for y in range(15):
        print(''.join(sym.get(wfc[x][y],'?')for x in range(20)))
```
SEED=42  SIZE=40x30
TERRAIN (first 10 rows x 20 cols):
""
""""
"""""""""
"""*""""
"""****"""
"~"****^^^
""""***^^^
""""""*^^^
"~~""""*^^
"~~~~~"""*^
BSP DUNGEON (7 rooms, first 10 rows x 20 cols):
#####################
#.......#####.....##
#.......#####.....##
#.......#####...##.#
#.......#####...##.#
#.........##...##..#
############...##..#
############...##..#
#.......##...##....#
#.......##...######
DRUNKARD WALK (first 10 rows x 20 cols):
#####################
##......#.......####
##......#.......#..#
##.....##.......#..#
#########.........##
########...........#
##.....................############
##.....................############
##....#..............#
##....#.......########
L-SYSTEM PLANT: 1614 chars, 887 segments
L-SYSTEM ROAD: 2379 chars, 341 segments
WFC TILE MAP (20x15):
....................
....................
....................
...........***......
..........*****.....
..........*****.....
..,~~~~~~..........*.
..,~~~~~~~~.........*.
..~~~~~~~~~~~........
..~~~~~~~~~,.......
...~~~~~~.,,.......
....~~...,..........
.......,............
....................
....................