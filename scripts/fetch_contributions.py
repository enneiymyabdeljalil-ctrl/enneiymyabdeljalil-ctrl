#!/usr/bin/env python3
"""Refresh contribution data through GitHub GraphQL (requires GH_PAT: read:user)."""
import os,json,sys
from pathlib import Path
from datetime import date,datetime,timedelta,timezone
from collections import Counter
from urllib.request import Request,urlopen
token=os.getenv("GH_PAT")
if not token: sys.exit("Add repository secret GH_PAT with read:user permission, then rerun this workflow.")
today=date.today()
query="""query($login:String!,$from:DateTime!,$to:DateTime!){user(login:$login){contributionsCollection(from:$from,to:$to){contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}"""
body={"query":query,"variables":{"login":"enneiymyabdeljalil-ctrl","from":(today-timedelta(days=364)).isoformat()+"T00:00:00Z","to":today.isoformat()+"T23:59:59Z"}}
req=Request("https://api.github.com/graphql",data=json.dumps(body).encode(),headers={"Authorization":"Bearer "+token,"Content-Type":"application/json","User-Agent":"profile-readme-cards"})
with urlopen(req,timeout=30) as r: result=json.loads(r.read().decode())
if result.get("errors") or not result.get("data",{}).get("user"): sys.exit("GraphQL error: "+json.dumps(result.get("errors")))
cal=result["data"]["user"]["contributionsCollection"]["contributionCalendar"]
days=[d for w in cal["weeks"] for d in w["contributionDays"]]
active=[d for d in days if d["contributionCount"]>0]
monthly=Counter(); weekdays=Counter()
for d in days:
 monthly[d["date"][:7]]+=d["contributionCount"]
 if d["contributionCount"]: weekdays[datetime.strptime(d["date"],"%Y-%m-%d").strftime("%A")]+=d["contributionCount"]
dates={date.fromisoformat(d["date"]) for d in active}; cursor=today if today in dates else today-timedelta(days=1); streak=0
while cursor in dates: streak+=1; cursor-=timedelta(days=1)
out={"year":today.year,"total":cal["totalContributions"],"active_days":len(active),"streak":streak,
"busiest_day":weekdays.most_common(1)[0][0] if weekdays else "No activity yet",
"days":[{"date":d["date"],"count":d["contributionCount"]} for d in days],
"monthly":dict(monthly),"updated_at":datetime.now(timezone.utc).isoformat()}
Path("data/contributions.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
print("Updated contribution data:",out["total"],"contributions")
