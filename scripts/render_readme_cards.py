#!/usr/bin/env python3
"""Render the animated Profile Signal Kit SVG cards."""
import json
import os
from datetime import date, timedelta
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "cards"
STATIC = os.getenv("STATIC") == "1"
BG, PANEL, DARK = "#080d18", "#101a2b", "#0b1220"
LINE, CYAN, BLUE, VIOLET = "#27364c", "#5ee7f5", "#60a5fa", "#a78bfa"
WHITE, MUTED = "#f1f5f9", "#9aa9bd"

try:
    DATA = json.loads((ROOT / "data/contributions.json").read_text(encoding="utf-8"))
except Exception:
    DATA = {"total": None, "active_days": None, "streak": None,
            "busiest_day": "—", "days": [], "monthly": {}}


def start(width, height):
    css = "" if STATIC else """<style>
    text{font-family:Inter,Arial,sans-serif}
    .reveal{opacity:0;animation:rise .75s ease-out .15s forwards}
    .reveal2{opacity:0;animation:rise .75s ease-out .35s forwards}
    .pulse{animation:pulse 2s ease-in-out infinite}
    .cursor{animation:blink 1s steps(2,start) infinite}
    @keyframes rise{to{opacity:1;transform:translateY(0)}from{opacity:0;transform:translateY(12px)}}
    @keyframes pulse{0%,100%{opacity:1}50%{opacity:.35}}
    @keyframes blink{50%{opacity:0}}
    @media(prefers-reduced-motion:reduce){.reveal,.reveal2,.pulse,.cursor{animation:none!important;opacity:1!important;transform:none!important}}
    </style>"""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}">{css}'
            f'<defs><linearGradient id="panel" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#14243a"/><stop offset="1" stop-color="#0b1220"/>'
            '</linearGradient><linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">'
            '<stop offset="0" stop-color="#5ee7f5"/><stop offset="1" stop-color="#a78bfa"/>'
            '</linearGradient><pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">'
            '<circle cx="1" cy="1" r="1" fill="#7690ae" opacity=".18"/></pattern></defs>'
            f'<rect width="{width}" height="{height}" rx="24" fill="{BG}"/>')


def box(x, y, width, height, fill=PANEL, stroke=LINE, radius=18):
    return (f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
            f'rx="{radius}" fill="{fill}" stroke="{stroke}"/>')


def text(x, y, value, size=16, color=WHITE, weight=400, spacing=0):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
            f'font-weight="{weight}" letter-spacing="{spacing}">{escape(str(value))}</text>')


def save(name, svg):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(svg + "</svg>\n", encoding="utf-8")


def render_hero():
    s = start(1000, 330) + box(2, 2, 996, 326, "url(#panel)", "#2b405b", 24)
    s += '<rect x="2" y="2" width="996" height="326" rx="24" fill="url(#dots)"/>'
    s += '<circle cx="890" cy="82" r="112" fill="#5ee7f5" opacity=".045"/>'
    s += '<circle cx="920" cy="270" r="150" fill="#a78bfa" opacity=".055"/>'
    s += '<g class="reveal">'
    s += text(42, 52, "ABDELJALIL ENNEIYMY  /  DEVELOPER PROFILE", 12, CYAN, 700, 1.8)
    s += text(42, 119, "Building the web,", 43, WHITE, 750)
    s += text(42, 169, "one project at a time.", 43, WHITE, 750)
    s += text(44, 215, "Full-Stack Development Student", 19, "#cbd5e1", 600)
    s += text(44, 249, "OFPPT  ·  Morocco  ·  Learning by building", 14, MUTED)
    s += '<rect x="43" y="278" width="190" height="29" rx="14" fill="#0b2632" stroke="#1e5966"/>'
    s += '<circle class="pulse" cx="60" cy="292" r="4" fill="#5ee7f5"/>'
    s += text(73, 297, "CURRENTLY LEARNING", 10, CYAN, 700, 1)
    s += '</g><g class="reveal2">'
    s += box(620, 35, 337, 260, DARK, "#30435c", 17)
    s += '<path d="M620 76 H957" stroke="#26364b"/>'
    for x, color in [(643, "#fb7185"), (661, "#fbbf24"), (679, "#4ade80")]:
        s += f'<circle cx="{x}" cy="56" r="5" fill="{color}"/>'
    s += text(704, 60, "abdeljalil@dev  ~", 12, MUTED, 600)
    s += text(645, 112, "$ whoami", 13, CYAN, 600)
    s += text(645, 143, "full-stack developer in training", 14)
    s += text(645, 185, "$ stack --now", 13, CYAN, 600)
    s += text(645, 214, "React   Redux   JavaScript", 13, "#dbeafe")
    s += text(645, 239, "PHP     MySQL    MongoDB", 13, "#dbeafe")
    s += text(645, 273, "$ build --keep-going", 13, CYAN, 600)
    s += '<rect class="cursor" x="830" y="261" width="8" height="15" rx="1" fill="#5ee7f5"/>'
    s += '</g>'
    save("hero.svg", s)


def render_status():
    s = start(1000, 118) + box(2, 2, 996, 114, "url(#panel)", LINE, 20)
    rows = [(30, "01  /  STATUS", "Student developer", CYAN),
            (354, "02  /  ENVIRONMENT", "OFPPT · Morocco", BLUE),
            (678, "03  /  METHOD", "Learn → Build → Improve", VIOLET)]
    for x, label, value, color in rows:
        s += f'<g class="reveal">{text(x,43,label,10,color,700,1.2)}{text(x,78,value,19,WHITE,650)}</g>'
    s += '<path d="M320 25 V92 M644 25 V92" stroke="#27364c"/>'
    save("status.svg", s)


def render_focus():
    s = start(1000, 226) + text(24, 31, "CURRENT FOCUS", 11, CYAN, 700, 2)
    s += text(24, 57, "What I'm practicing right now", 18, WHITE, 650)
    cards = [(24,"01","FRONTEND","React · Redux · JavaScript",CYAN,"Build interfaces and manage state"),
             (347,"02","BACKEND","PHP · MySQL",BLUE,"Practice server-side logic and data"),
             (670,"03","DATABASES","SQL · MongoDB",VIOLET,"Query, model, and organize information")]
    for x, number, heading, stack, color, description in cards:
        s += box(x,76,306,132)
        s += f'<g class="reveal2">{text(x+18,103,number,11,color,700)}'
        s += text(x+18,133,heading,12,MUTED,700,1.3)
        s += text(x+18,164,stack,17,WHITE,650)
        s += text(x+18,190,description,11,MUTED) + '</g>'
    save("focus.svg", s)


def render_project(filename, title, category, description, stack, url, accent):
    s = start(500,190) + f'<a href="{escape(url)}">' + box(2,2,496,186)
    s += f'<rect x="2" y="2" width="5" height="186" rx="2" fill="{accent}"/>'
    s += '<g class="reveal">'
    s += text(27,35,category,10,accent,700,1.5)
    s += text(27,78,title,25,WHITE,700)
    s += text(27,111,description,12,MUTED)
    s += '<rect x="27" y="132" width="175" height="29" rx="14" fill="#19283d"/>'
    s += text(41,151,stack,11,"#d7e5f5",600)
    s += text(355,166,"VIEW REPO  ↗",10,accent,700,.8)
    s += '</g></a>'
    save(filename, s)


def render_activity():
    s = start(1000,286) + box(2,2,996,282,"url(#panel)",LINE,20)
    s += text(28,39,"GITHUB ACTIVITY",11,CYAN,700,1.8)
    s += text(28,65,"Contribution rhythm · last 12 months",15,WHITE,600)
    today = date.today()
    months = []
    for n in range(11,-1,-1):
        year, month = today.year, today.month - n
        while month <= 0:
            year -= 1
            month += 12
        months.append((year,month))
    values = [int(DATA.get("monthly",{}).get(f"{y}-{m:02d}",0)) for y,m in months]
    maximum = max(values + [1])
    for i, ((year,month), value) in enumerate(zip(months,values)):
        x = 30 + i*76
        height = 112*value/maximum if value else 3
        s += f'<rect x="{x}" y="{205-height:.1f}" width="42" height="{height:.1f}" rx="6" fill="url(#accent)" opacity=".88"/>'
        s += text(x,226,date(year,month,1).strftime("%b"),10,MUTED)
    stats = [("TOTAL CONTRIBUTIONS",DATA.get("total")),
             ("ACTIVE DAYS",DATA.get("active_days")),
             ("CURRENT STREAK",DATA.get("streak"))]
    for i, (label,value) in enumerate(stats):
        x = 30 + i*315
        s += text(x,263,label,9,MUTED,700,.8)
        s += text(x+190,263,"—" if value is None else value,14,WHITE,700)
    save("activity.svg", s)


def render_contributions():
    s = start(1000,190) + box(2,2,996,186,"url(#panel)",LINE,20)
    s += text(28,34,"CONTRIBUTION MAP",11,CYAN,700,1.8)
    s += text(28,56,"Daily activity · last 365 days",13,WHITE,500)
    by_date = {item["date"]:int(item["count"]) for item in DATA.get("days",[]) if "date" in item}
    begin = date.today() - timedelta(days=364)
    palette = ["#19283a","#164e63","#0e7490","#0891b2","#5ee7f5"]
    for i in range(365):
        day = begin + timedelta(days=i)
        count = by_date.get(day.isoformat(),0)
        level = 0 if count == 0 else 1 if count < 2 else 2 if count < 5 else 3 if count < 9 else 4
        x, y = 29+(i//7)*17, 75+(i%7)*14
        s += f'<rect x="{x}" y="{y}" width="11" height="10" rx="2" fill="{palette[level]}"/>'
    s += text(30,179,"LESS",9,MUTED,600,1) + text(910,179,"MORE",9,MUTED,600,1)
    save("contributions.svg", s)


def main():
    render_hero()
    render_status()
    render_focus()
    render_project("project-react.svg","React_2","FRONTEND PRACTICE",
                   "React coursework and hands-on exercises","React · JavaScript",
                   "https://github.com/enneiymyabdeljalil-ctrl/React_2",CYAN)
    render_project("project-sql.svg","DATABASE_SQL-","DATABASE PRACTICE",
                   "SQL database exercises and query practice","SQL · MySQL",
                   "https://github.com/enneiymyabdeljalil-ctrl/DATABASE_SQL-",VIOLET)
    render_activity()
    render_contributions()
    print("Rendered Profile Signal Kit cards. STATIC=" + str(STATIC))


if __name__ == "__main__":
    main()
