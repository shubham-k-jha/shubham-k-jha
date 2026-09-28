# AUTO-GENERATED VISUAL TEMPLATE MODE
# The profile README is maintained as README.template.md for the visual layer.
# The API/classifier engine can still update data/repositories.json.
#!/usr/bin/env python3
import json, os, sys, urllib.request
from pathlib import Path
ROOT=Path(__file__).parent
CFG=json.loads((ROOT/'config.json').read_text())
CACHE=ROOT/'data/repositories.json'

def get(url):
    req=urllib.request.Request(url,headers={'Accept':'application/vnd.github+json','User-Agent':'shubham-k-jha-profile-generator'})
    if os.getenv('GITHUB_TOKEN'): req.add_header('Authorization','Bearer '+os.getenv('GITHUB_TOKEN'))
    with urllib.request.urlopen(req,timeout=30) as r: return json.load(r)

def repos():
    try:
        out=[]; page=1
        while True:
            b=get(f"https://api.github.com/users/{CFG['username']}/repos?per_page=100&page={page}&sort=updated")
            if not b: break
            out+=b
            if len(b)<100: break
            page+=1
        CACHE.write_text(json.dumps(out,indent=2))
        return out
    except Exception as e:
        print('[WARN] API unavailable; using cached data:',e,file=sys.stderr)
        return json.loads(CACHE.read_text())

def classify(r):
    if r['name'] in CFG['overrides']: return CFG['overrides'][r['name']]
    text=' '.join([r.get('name',''),r.get('description','') or '', ' '.join(r.get('topics') or []),r.get('language','') or '']).lower()
    result=[]
    for k,v in CFG['categories'].items():
        hits=sum(kw.lower() in text for kw in v['keywords'])
        if hits/max(3,len(v['keywords'])) >= CFG['classification']['minimum_score']: result.append(k)
    return result[:4]

def card(r):
    title=r['name'].replace('-',' ').replace('_',' ').title()
    return f"### 📦 [{title}]({r['html_url']})\n{r.get('description') or 'GitHub repository'}\n\n`{r.get('language') or '—'}` · ⭐ {r.get('stargazers_count',0)} · 🍴 {r.get('forks_count',0)}"

def main():
    rs=[r for r in repos() if r.get('name') not in CFG['exclude']]
    by={k:[] for k in CFG['categories']}
    for r in rs:
        for c in classify(r): by[c].append(r)
    lookup={r['name']:r for r in rs}
    featured=[lookup[n] for n in CFG['featured'] if n in lookup]
    cards=[]
    for k,v in CFG['categories'].items(): cards.append(f"<td align='center' width='25%'><h3>{v['label']}</h3><b>{len(by[k])} project{'s' if len(by[k])!=1 else ''}</b><br><a href='#cat-{k}'>EXPLORE →</a></td>")
    nav='<tr>'+''.join(cards[:4])+'</tr><tr>'+''.join(cards[4:])+'</tr>'
    fh='\n\n'.join(card(r) for r in featured)
    sections=[]
    for k,v in CFG['categories'].items():
        rows='\n'.join(f"| [{r['name']}]({r['html_url']}) | {r.get('description') or 'Repository'} |" for r in by[k]) or '| — | No repositories currently match. |'
        sections.append(f"<a id='cat-{k}'></a>\n## {v['label']}\n\n| Repository | Description |\n|---|---|\n{rows}")
    games='\n'.join(f"<td align='center'><h3>{g['icon']} {g['name']}</h3><a href='{g['live']}'><b>▶ PLAY LIVE</b></a><br><a href='{g['repo']}'>SOURCE CODE →</a></td>" for g in CFG['games'])
    readme=f"""# 👋 Shubham Jha\n\n### `Research → Data Analytics → Data Science`\n\n**Data Analyst · Python & SQL · Power BI · Scientific Computing · Aspiring Data Scientist**\n\n<p><a href='{CFG['website_url']}'>🌐 Portfolio</a> · <a href='{CFG['profile_url']}'>💻 GitHub</a> · <a href='https://www.linkedin.com/in/shubham-k-jha/'>💼 LinkedIn</a> · <a href='mailto:sjha31190@gmail.com'>✉️ Email</a></p>\n\n> I turn messy data into analysis, models, dashboards and reproducible workflows — combining scientific research discipline with practical analytics.\n\n---\n\n## ⚡ Explore the Portfolio\n\n<table width='100%'>{nav}</table>\n\n---\n\n## 🎯 What I Build\n\n| Track | Focus |\n|---|---|\n| 📊 **Analytics** | EDA, KPIs, business questions, customer/revenue analysis |\n| 🗄️ **SQL** | Joins, CTEs, window functions, cleaning, relational analysis |\n| 📈 **BI** | Power BI dashboards, visual storytelling, reporting |\n| 🤖 **Data Science** | Classification, regression, feature engineering, evaluation |\n| 🐍 **Python** | Pandas, NumPy, SciPy, automation, reproducible pipelines |\n| 🔬 **Research** | Solar active regions, scientific datasets, statistics, time series |\n\n---\n\n## ⭐ Featured Work\n\n{fh}\n\n---\n\n## 🧰 Stack\n\n**Data:** Python · Pandas · NumPy · SciPy · SQL  \n**BI / Viz:** Power BI · Matplotlib · Seaborn · Plotly  \n**Databases:** PostgreSQL · MySQL · SQLite  \n**ML:** Scikit-learn · XGBoost · SHAP  \n**Big Data / Apps:** PySpark · Apache Spark · Streamlit · AWS fundamentals  \n**Scientific:** SunPy · Astropy · IDL · Jupyter · Linux  \n**Workflow:** Git · GitHub · GitHub Actions\n\n---\n\n## 🎮 Game Lab\n\n<table width='100%'><tr>{games}</tr></table>\n\n---\n\n## 🔬 Research → Data\n\nMy research work is built around large scientific datasets, quantitative analysis, visualization and domain-informed modelling. The same workflow carries into analytics:\n\n**Question → Clean → Explore → Validate → Model → Explain → Ship**\n\n---\n\n## 🚀 Current Direction\n\n**Target:** Data Analyst · BI / Business Analyst · Research Data Analyst · Data Science roles  \n**Strengthening:** Advanced SQL · Machine Learning · PySpark / Spark · Statistics · AWS · Data Engineering fundamentals\n\n---\n\n## 📚 Live Repository Map\n\nThese sections are generated from GitHub repository metadata. Explicit overrides in `config.json` take precedence.\n\n{'\n\n'.join(sections)}\n\n---\n\n## 🧭 Career Snapshot\n\n**Physics → Scientific Research → Research Data Analysis → Data Analytics → Data Science**\n\nM.Sc. Physics · GATE (Physics) · Research experience at Indian Institute of Astrophysics and NIT Delhi\n\n---\n\n## 🛠️ Automation\n\n`GitHub API → metadata → classifier → overrides → generated README → GitHub Actions`\n\n- `generate_readme.py` — actual generator\n- `config.json` — weights, categories, overrides, featured projects\n- `data/repositories.json` — cached API fallback\n- `.github/workflows/update-readme.yml` — scheduled + manual refresh\n- `portfolio/` — real JavaScript dashboard for category filtering\n\n---\n\n## 🤝 Connect\n\nOpen to opportunities in **Data Analytics, BI, Research Data Analysis, Data Science and related data roles**.\n\n**🌐 Portfolio:** {CFG['website_url']}  \n**💻 GitHub:** {CFG['profile_url']}  \n**💼 LinkedIn:** https://www.linkedin.com/in/shubham-k-jha/  \n**✉️ Email:** sjha31190@gmail.com\n\n<sub>Generated from GitHub metadata with human-controlled overrides.</sub>\n"""
    (ROOT/'README.md').write_text(readme)
    print(f'Generated README from {len(rs)} repositories.')
if __name__=='__main__': main()
