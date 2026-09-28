#!/usr/bin/env python3
"""
Generate a GitHub profile README from live public repository metadata.

Requirements:
  pip install requests pyyaml

Environment:
  GITHUB_TOKEN (recommended in GitHub Actions; public unauthenticated calls
  also work but have lower API limits)

Run:
  python generate_readme.py
"""

from __future__ import annotations
import os, re, json
from pathlib import Path
from typing import Any
import requests
import yaml

ROOT = Path(__file__).resolve().parent
CONFIG = yaml.safe_load((ROOT / "config.yaml").read_text())
README_TEMPLATE = (ROOT / "README.template.md").read_text()
OUT = ROOT / "README.md"

API = "https://api.github.com"
USERNAME = CONFIG["username"]
WEIGHTS = CONFIG["classification"]["weights"]
THRESHOLD = float(CONFIG["classification"].get("threshold", 0.35))
CATEGORIES = CONFIG["categories"]
OVERRIDES = CONFIG.get("overrides", {})
EXCLUDE = set(CONFIG.get("exclude", []))

session = requests.Session()
session.headers.update({"Accept": "application/vnd.github+json"})
if os.getenv("GITHUB_TOKEN"):
    session.headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"


def api_get(url: str, **params) -> Any:
    r = session.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def get_repositories() -> list[dict]:
    repos = []
    page = 1
    while True:
        batch = api_get(f"{API}/users/{USERNAME}/repos", per_page=100, page=page, type="all", sort="updated")
        if not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return repos


def readme_text(repo: dict) -> str:
    try:
        r = session.get(repo["contents_url"].replace("{+path}", "/README.md"), timeout=20)
        if r.status_code != 200:
            return ""
        import base64
        return base64.b64decode(r.json().get("content", "")).decode("utf-8", errors="ignore")[:12000]
    except requests.RequestException:
        return ""


def norm(x: Any) -> str:
    return str(x or "").lower().replace("_", "-").strip()


def category_score(repo: dict, keyword: str, readme: str) -> float:
    kw = norm(keyword)
    name = norm(repo["name"])
    desc = norm(repo.get("description"))
    topics = [norm(x) for x in repo.get("topics", [])]
    languages = [norm(x) for x in (repo.get("language") or "").split(",") if x]
    # For a single primary language, the language signal is intentionally weak.
    fields = {
        "topics": " ".join(topics),
        "name": name,
        "description": desc,
        "readme": norm(readme),
        "languages": " ".join(languages),
    }
    score = 0.0
    for field, text in fields.items():
        if kw and kw in text:
            score += WEIGHTS[field]
    return score


def classify(repo: dict, readme: str) -> list[str]:
    name = repo["name"]
    if name in OVERRIDES and "categories" in OVERRIDES[name]:
        return OVERRIDES[name]["categories"]
    scores = {}
    for slug, meta in CATEGORIES.items():
        scores[slug] = max(
            (category_score(repo, kw, readme) for kw in meta.get("keywords", [])),
            default=0.0,
        )
    return [slug for slug, score in scores.items() if score >= THRESHOLD]


def quality_score(repo: dict) -> float:
    # Ranking aid only; not a quality verdict.
    return (
        (1.0 if repo.get("has_wiki") is not None else 0.0) * 0.05
        + min(len(repo.get("description") or "") / 120, 1) * 0.20
        + min(repo.get("stargazers_count", 0) / 10, 1) * 0.10
        + min(repo.get("forks_count", 0) / 5, 1) * 0.05
        + (0.6 if not repo.get("archived") else 0.0) * 0.60
    )


def card(repo: dict) -> str:
    name = repo["name"]
    desc = (repo.get("description") or "No repository description provided.").replace("|", "\\|")
    lang = repo.get("language") or "—"
    topics = " · ".join(repo.get("topics", [])[:4])
    meta = f"`{lang}`"
    if topics:
        meta += f" · {topics}"
    links = f"[View Repository →]({repo['html_url']})"
    if repo.get("homepage"):
        links += f" · [Live Demo →]({repo['homepage']})"
    return (
        f"**📦 [{name}]({repo['html_url']})**  \n"
        f"{desc}  \n"
        f"{meta}  \n"
        f"⭐ {repo.get('stargazers_count',0)} · 🔀 {repo.get('forks_count',0)} · {links}"
    )


def replace_marker(text: str, marker: str, content: str) -> str:
    start = f"<!-- AUTO:{marker}:START -->"
    end = f"<!-- AUTO:{marker}:END -->"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    replacement = f"{start}\n{content}\n{end}"
    return pattern.sub(replacement, text)


def main():
    repos = get_repositories()
    live = []
    for repo in repos:
        if repo.get("fork") or repo.get("name") in EXCLUDE:
            continue
        repo["topics"] = api_get(f"{API}/repos/{USERNAME}/{repo['name']}/topics").get("names", [])
        rm = readme_text(repo)
        repo["categories"] = classify(repo, rm)
        repo["featured"] = bool(OVERRIDES.get(repo["name"], {}).get("featured", False))
        live.append(repo)

    text = README_TEMPLATE.replace("USERNAME", USERNAME)

    featured = [r for r in live if r["featured"]]
    featured.sort(key=quality_score, reverse=True)
    featured_md = "\n\n".join(card(r) for r in featured[:6]) or "_No featured repositories configured yet._"
    text = replace_marker(text, "FEATURED", featured_md)

    for slug in CATEGORIES:
        items = [r for r in live if slug in r.get("categories", [])]
        items.sort(key=quality_score, reverse=True)
        body = "\n\n".join(card(r) for r in items) or "_No repositories currently classified in this category._"
        text = replace_marker(text, f"CATEGORY:{slug}", body)

    active = [
        r for r in live
        if any(k in " ".join([r["name"], r.get("description") or "", *r.get("topics", [])]).lower()
               for k in ["active", "in-progress", "wip", "learning"])
    ]
    active.sort(key=lambda r: r.get("pushed_at") or "", reverse=True)
    active_md = "\n\n".join(card(r) for r in active[:8]) or "_No repositories currently match the active/WIP signals._"
    text = replace_marker(text, "ACTIVE", active_md)

    (ROOT / "data/repositories.json").write_text(json.dumps(live, indent=2, ensure_ascii=False))
    OUT.write_text(text)
    print(f"Generated {OUT} from {len(live)} public repositories.")


if __name__ == "__main__":
    main()
