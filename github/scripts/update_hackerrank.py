#!/usr/bin/env python3
# .github/scripts/update_hackerrank.py

import requests
from bs4 import BeautifulSoup
import re
import sys
from datetime import datetime

USERNAME = "anand7061"   # Your HackerRank username
README_PATH = "README.md"
START_MARK = "<!-- HACKERRANK-STATS:START -->"
END_MARK = "<!-- HACKERRANK-STATS:END -->"

def fetch_profile_html(username):
    url = f"https://www.hackerrank.com/{username}"
    headers = {"User-Agent": "github-action-hackerrank-stats/1.0"}
    r = requests.get(url, headers=headers, timeout=15)
    r.raise_for_status()
    return r.text

def parse_stats(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)

    # Score / Rating
    score = None
    m = re.search(r"(?:Score|Rating)[^\d]*(\d{2,6}(?:\.\d+)?)", text, re.I)
    if m:
        score = m.group(1)

    # Badges
    badges = None
    try:
        badge_elems = soup.select("ul.badge-list li, .profile-badges .badge, .badge")
        if badge_elems:
            badges = len(badge_elems)
        else:
            m2 = re.search(r"Badges?\s*[:\-\s]*\s*(\d+)", text, re.I)
            if m2:
                badges = int(m2.group(1))
    except Exception:
        badges = None

    # Problems solved
    solved = None
    m3 = re.search(r"Solved\s*(\d+)", text, re.I)
    if m3:
        solved = m3.group(1)

    return {"score": score, "badges": badges, "solved": solved}

def build_markdown(stats):
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    lines = []
    lines.append(f"**HackerRank profile — [{USERNAME}](https://www.hackerrank.com/{USERNAME})**  ")
    if stats.get("score"):
        lines.append(f"- **Score / Rating:** {stats['score']}  ")
    if stats.get("badges") is not None:
        lines.append(f"- **Badges:** {stats['badges']}  ")
    if stats.get("solved"):
        lines.append(f"- **Problems solved:** {stats['solved']}  ")
    lines.append(f"_Last updated: {now}_")
    return "\n".join(lines)

def replace_readme_block(readme_path, new_block):
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
    start = content.find(START_MARK)
    end = content.find(END_MARK)
    if start == -1 or end == -1:
        print("Markers not found in README.md", file=sys.stderr)
        sys.exit(1)
    new_content = content[:start+len(START_MARK)] + "\n" + new_block + "\n" + content[end:]
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Updated README.md")

def main():
    html = fetch_profile_html(USERNAME)
    stats = parse_stats(html)
    md = build_markdown(stats)
    replace_readme_block(README_PATH, md)

if __name__ == "__main__":
    main()
