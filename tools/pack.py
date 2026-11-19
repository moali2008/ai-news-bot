import json,math
d=json.load(open('raw.json'));LAT0=(34.0425+34.0575)/2;LON0=(-118.2635-118.2425)/2
kx=111320*math.cos(math.radians(LAT0));ky=110540
P=lambda g:[round((p['lon']-LON0)*kx,1) for p in g]
def pts(g):
    o=[]
    for p in g:o+= [round((p['lon']-LON0)*kx,1),round(-(p['lat']-LAT0)*ky,1)]
    return o
def num(v):
    try:return float(str(v).replace('m','').replace(';','.').split()[0])
    except:return None
R=[];B=[];A=[];T=[]
for e in d['elements']:
    t=e.get('tags',{})
    if e['type']=='node':
        T+=[round((e['lon']-LON0)*kx,1),round(-(e['lat']-LAT0)*ky,1)];continue
    geoms=[]
    if e['type']=='way' and 'geometry' in e:geoms=[e['geometry']]
    elif e['type']=='relation':geoms=[m['geometry'] for m in e.get('members',[]) if m.get('role')=='outer' and 'geometry' in m]
    for g in geoms:
        if 'highway' in t and e['type']=='way':
            R.append([t['highway'],t.get('name',''),num(t.get('lanes')) or 0,1 if t.get('oneway')=='yes' else 0,num(t.get('width')) or 0,1 if t.get('bridge') else 0,1 if t.get('tunnel') else 0,int(num(t.get('layer')) or 0),pts(g)])
        elif 'building' in t or 'building:part' in t:
            h=num(t.get('height'));lv=num(t.get('building:levels'));mh=num(t.get('min_height')) or 0
            B.append([round(h,1) if h else (round(lv*3.4,1) if lv else 0),round(mh,1),t.get('name',''),t.get('building',''),t.get('building:colour',''),pts(g)])
        else:
            A.append([t.get('leisure') or t.get('landuse') or t.get('area:highway') or '',t.get('name',''),pts(g)])
json.dump({'c':[LAT0,LON0],'r':R,'b':B,'a':A,'t':T,'src':'© OpenStreetMap contributors, ODbL'},open('la.json','w'),ensure_ascii=False,separators=(',',':'))
print(len(R),'roads',len(B),'buildings',len(A),'areas',len(T)//2,'trees')
