#!/usr/bin/env python3
"""Render README SVG cards. STATIC=1 disables all motion for screenshots."""
import os, json, base64, subprocess
from pathlib import Path
from datetime import date, timedelta
from xml.sax.saxutils import escape

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/"cards"
try: DATA=json.loads((ROOT/"data/contributions.json").read_text())
except Exception: DATA={"total":None,"active_days":None,"streak":None,"busiest_day":"—","days":[],"monthly":{}}
STATIC=os.getenv("STATIC")=="1"
BG="#08111f"; PANEL="#101e31"; BLUE="#38bdf8"; CYAN="#67e8f9"; WHITE="#e5f3ff"; MUTED="#91a7bd"
font=""
fontfile=ROOT/"assets/Inter-Regular.ttf"
if fontfile.exists():
    try:
        out=OUT/"inter-subset.woff2"; OUT.mkdir(exist_ok=True)
        subprocess.run(["pyftsubset",str(fontfile),"--output-file="+str(out),"--flavor=woff2","--unicodes=U+0000-00FF"],check=True,capture_output=True)
        font="@font-face{font-family:InterEmbedded;src:url(data:font/woff2;base64,"+base64.b64encode(out.read_bytes()).decode()+") format('woff2')}"
    except Exception: pass
def start(w,h,delay=0):
    css="" if STATIC else f"""<style>{font} text{{font-family:InterEmbedded,Inter,Arial,sans-serif}} .in{{opacity:0;animation:up .8s ease-out {delay}s forwards}} @keyframes up{{to{{opacity:1;transform:translateY(0)}}from{{opacity:0;transform:translateY(16px)}}}} @media(prefers-reduced-motion:reduce){{.in{{animation:none!important;opacity:1!important;transform:none!important}}}}</style>"""
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{css}<rect width="100%" height="100%" rx="22" fill="{BG}"/>'
def t(x,y,s,size=16,color=WHITE,weight=400):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}">{escape(str(s))}</text>'
def save(name,s): OUT.mkdir(parents=True,exist_ok=True); (OUT/name).write_text(s+"</svg>\n",encoding="utf-8")
def tile(name,title,sub,url,color,delay):
    s=start(320,130,delay)+f'<a href="{url}"><rect x="2" y="2" width="316" height="126" rx="18" fill="{PANEL}" stroke="{color}" stroke-opacity=".65"/><g class="in">{t(25,52,title,22,WHITE,700)}{t(25,86,sub,13,MUTED)}{t(278,110,"↗",18,color,700)}</g></a>'
    save(name,s)
def main():
    s=start(1000,250,0)+'<rect x="2" y="2" width="996" height="246" rx="22" fill="#102b45" stroke="#24445f"/>'
    s+=f'<g class="in">{t(48,65,"HELLO, I’M",14,CYAN,700)}{t(48,127,"Abdeljalil Enneiymy",43,WHITE,700)}{t(50,172,"Full-Stack Development Student · OFPPT, Morocco",20,"#c5d9eb")}{t(50,211,"Learning, building, and improving one project at a time.",15,MUTED)}</g>'
    save("hero.svg",s)
    tile("tile-build.svg","BUILD","React · JavaScript · PHP","https://github.com/enneiymyabdeljalil-ctrl",BLUE,.2)
    tile("tile-learn.svg","LEARN","SQL · MongoDB · Python","https://github.com/enneiymyabdeljalil-ctrl?tab=repositories",CYAN,.4)
    tile("tile-projects.svg","PROJECTS","Explore public repositories","https://github.com/enneiymyabdeljalil-ctrl?tab=repositories","#a78bfa",.6)
    s=start(1000,300,1.0)+t(32,43,"CONTRIBUTION ACTIVITY",17,CYAN,700)
    months=[]; today=date.today()
    for n in range(11,-1,-1):
        y,m=today.year,(today.month-n)
        while m<=0: y-=1; m+=12
        months.append((y,m))
    vals=[int(DATA.get("monthly",{}).get(f"{y}-{m:02d}",0)) for y,m in months]; mx=max(vals+[1])
    for i,((y,m),v) in enumerate(zip(months,vals)):
        x=35+i*78; h=120*v/mx
        s+=f'<rect x="{x}" y="{210-h:.1f}" width="42" height="{h:.1f}" rx="6" fill="{BLUE}"/>'
        s+=t(x,235,date(y,m,1).strftime("%b"),11,MUTED)
    for i,(label,key) in enumerate([("TOTAL","total"),("ACTIVE DAYS","active_days"),("STREAK","streak")]):
        x=38+i*300; v=DATA.get(key)
        s+=t(x,278,label,10,MUTED,700)+t(x+105,278,"—" if v is None else v,16,WHITE,700)
    s+=t(760,43,"BUSIEST DAY",10,MUTED,700)+t(760,70,DATA.get("busiest_day","—"),17,WHITE,700)
    save("activity.svg",s)
    for filename,title,desc,lang,url,delay in [
      ("repo-react.svg","React_2","React coursework and practical exercises","JavaScript","https://github.com/enneiymyabdeljalil-ctrl/React_2",1.35),
      ("repo-sql.svg","DATABASE_SQL-","SQL database exercises and practice","SQL","https://github.com/enneiymyabdeljalil-ctrl/DATABASE_SQL-",1.65)]:
        s=start(1000,160,delay)+f'<a href="{url}"><rect x="2" y="2" width="996" height="156" rx="20" fill="{PANEL}" stroke="#24445f"/><g class="in">{t(32,46,"FEATURED REPOSITORY",11,CYAN,700)}{t(32,88,title,27,WHITE,700)}{t(32,124,desc,15,MUTED)}<rect x="820" y="60" width="140" height="34" rx="17" fill="#12334a"/>{t(845,83,lang,14,CYAN,700)}{t(905,137,"OPEN ↗",12,BLUE,700)}</g></a>'
        save(filename,s)
    s=start(1000,210,2.0)+t(32,40,"CONTRIBUTION GRAPH",16,CYAN,700)+t(32,66,"Daily activity · last 365 days",12,MUTED)
    bydate={x["date"]:int(x["count"]) for x in DATA.get("days",[]) if "date" in x}
    begin=today-timedelta(days=364); colors=["#17283a","#164e63","#0e7490","#0891b2",BLUE]
    for i in range(365):
        day=begin+timedelta(days=i); c=bydate.get(day.isoformat(),0); level=0 if c==0 else 1 if c<2 else 2 if c<5 else 3 if c<9 else 4
        s+=f'<rect x="{34+(i//7)*13}" y="{87+(i%7)*14}" width="9" height="9" rx="2" fill="{colors[level]}"/>'
    s+=t(35,196,"LESS",10,MUTED)+t(916,196,"MORE",10,MUTED)
    save("contributions.svg",s)
    print("Rendered SVG cards. STATIC="+str(STATIC))
if __name__=="__main__": main()
