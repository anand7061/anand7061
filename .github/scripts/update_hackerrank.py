def build_svg(stats):
    score = stats.get("score", "N/A")
    badges = stats.get("badges", "N/A")
    solved = stats.get("solved", "N/A")

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="450" height="150">
      <rect width="100%" height="100%" fill="#1a1b27"/>
      <text x="20" y="40" fill="#38bdae" font-size="22">HackerRank Stats</text>
      <text x="20" y="80" fill="#ffffff" font-size="16">Score / Rating: {score}</text>
      <text x="20" y="110" fill="#ffffff" font-size="16">Badges: {badges}</text>
      <text x="20" y="140" fill="#ffffff" font-size="16">Problems Solved: {solved}</text>
    </svg>"""

def main():
    html = fetch_profile_html(USERNAME)
    stats = parse_stats(html)

    # Update README
    md = build_markdown(stats)
    replace_readme_block(README_PATH, md)

    # Save SVG
    svg = build_svg(stats)
    with open("github-metrics.svg", "w", encoding="utf-8") as f:
        f.write(svg)
