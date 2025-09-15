#!/usr/bin/env python3
# .github/scripts/update_hackerrank.py

import sys
from datetime import datetime

USERNAME = "anandkumarchatr1"   # <-- your HackerRank username
README_PATH = "README.md"
START_MARK = "<!-- HACKERRANK-STATS:START -->"
END_MARK = "<!-- HACKERRANK-STATS:END -->"

def build_markdown():
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    lines = []
    lines.append(f"**HackerRank profile — [{USERNAME}](https://www.hackerrank.com/profile/{USERNAME})**  \n")
    lines.append("### 🏆 Badges")
    lines.append("![C++](https://img.shields.io/badge/C++-★★★-00599C?logo=c%2B%2B&logoColor=white)")
    lines.append("![Python](https://img.shields.io/badge/Python-★★-3776AB?logo=python&logoColor=white)")
    lines.append("![SQL](https://img.shields.io/badge/SQL-★★★★★-4479A1?logo=mysql&logoColor=white)")
    lines.append("![30 Days of Code](https://img.shields.io/badge/30_Days_of_Code-★-green?logo=hackerrank&logoColor=white)")
    lines.append("")
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
    md = build_markdown()
    replace_readme_block(README_PATH, md)

if __name__ == "__main__":
    main()
